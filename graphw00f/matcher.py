# -*- coding: utf-8 -*-
"""
graphw00f precision matcher.

Replaces the original first-match-wins boolean detection with a scored,
family-first model:

  1. A small fixed set of PROBES is sent ONCE each (response cached + reused),
     instead of re-issuing overlapping queries per engine (fewer requests,
     consistent responses).
  2. Every discriminator is a SIGNAL tagged with:
        - engine   : the specific server/vendor it points to
        - family   : the underlying GraphQL library (graphql-js, graphql-core,
                     graphql-ruby, graphql-java, webonyx-php, ...)
        - weight   : how uniquely it identifies the engine
        - kind     : how to evaluate it against a cached response
  3. Signals are scored. The library FAMILY is resolved from parser-dialect
     signals; the specific ENGINE only wins when a server-unique signal fires.
     When only family-level signals match we report the family + best guess
     with a low confidence instead of over-claiming a specific server.

Design goal: never attribute a specific server from an error string that the
whole library family emits (the classic graphw00f false-positive, e.g.
`Directive "@skip" ... is required` -> "apollo", which is really graphql-js).
"""

# ---------------------------------------------------------------------------
# Signal weights
# ---------------------------------------------------------------------------
UNIQUE = 100   # server/vendor-unique: extensions key, vendor root name, vendor-only error, federation SDL
STRONG = 60    # near-unique error phrasing that (practically) only this engine emits
FAMILY = 15    # identifies the underlying library family, NOT the specific server
WEAK   = 5     # weak corroboration (generic string, header hint)

# Confidence thresholds
CONF_HIGH_MIN = UNIQUE          # >=1 server-unique signal
CONF_MED_MIN  = STRONG          # >=1 strong signal
# below STRONG -> family-only -> 'low'

# ---------------------------------------------------------------------------
# Probes  (id -> GraphQL document).  '' means "send an empty/omitted query".
# Keep this set MINIMAL — every id here costs one request pair per target.
# ---------------------------------------------------------------------------
PROBES = {
  'typename':      'query { __typename }',
  'badkw':         'queryy { __typename }',                 # bad operation keyword -> parser dialect
  'empty':         '',                                       # empty document -> "must provide query" family
  'skip_q':        'query @skip { __typename }',             # directive misplaced on operation
  'deprecated_q':  'query @deprecated { __typename }',       # @deprecated on QUERY
  'deprecated_f':  'query { __typename @deprecated }',       # @deprecated on FIELD
  'unknown_dir_f': 'query { __typename @graphw00f }',        # unknown directive on field
  'cached_q':      'query @cached { __typename }',           # Hasura @cached
  'badfield':      'query { graphw00f }',                    # unknown root field -> leaks root type name
  'schema_nosel':  'query { __schema }',                     # missing selection set
  'skip_badarg':   'query { __typename @skip(aa: true) }',   # unknown arg to @skip (pg_graphql)
  'dup_dir':       'query @dup @dup { __typename }',         # duplicate directive
  'incl_bad':      'query { __typename @include(if: falsee) }',
  'bang':          'query ! { __typename }',                 # unexpected char (webonyx)
  'aaa':           'aaa',                                     # bare word document
  'federation':    'query { _service { sdl } }',             # Apollo Federation / supergraph tell
  'frag_unused':   'query {\n  __typename\n}\n\nfragment woof on __Schema {\n  directives { name }\n}',
  'frag_cycle':    'query {\n  __typename\n  ...A\n}\nfragment A on Query { ...B }\nfragment B on Query { ...A }',
  'subscription':  'subscription { __typename }',
  'alias_dollar':  'query {\n  alias1$1:__typename\n}',
  'curly':         'query {\n  __typename {\n}',             # dangling curly
  # special probes (dict form): raw JSON body / plain HTML GET
  'noquery':       {'__rawjson__': {}},                      # POST {} -> "must provide query" wrapper msg
  'query_int':     {'__rawjson__': {'query': 123}},          # non-string query -> Ariadne/Yoga/http type msgs
  'landing':       {'__get_html__': True},                   # GET base URL -> IDE landing page HTML
  'apq':           {'__rawjson__': {'extensions': {'persistedQuery': {'version': 1,
                    'sha256Hash': '0000000000000000000000000000000000000000000000000000000000000000'}}}},
  'extra_param':   {'__rawjson__': {'query': '{__typename}', 'graphw00f': 1}},  # Yoga rejects unknown body params
}

# ---------------------------------------------------------------------------
# Signal table.  Each entry:
#   (engine, family, weight, probe_id, kind, arg)
#
# kinds:
#   'msg'         arg = substring        -> error .message contains arg
#   'part'        arg = (field, sub)     -> error .<field> contains sub
#   'typename'    arg = value            -> data.__typename == value
#   'alias'       arg = (alias, value)   -> data[alias] == value
#   'field'       arg = (field, value)   -> data[field] == value
#   'ext_key'     arg = key              -> key present in top-level response.extensions
#   'ext_code'    arg = value            -> some error.extensions.code == value
#   'ext_field'   arg = (path.tuple,val) -> nested error.extensions field == value
#   'top'         arg = (key, sub)       -> top-level response[key] (str) contains sub
#   'federation'  arg = None             -> data._service.sdl is a non-empty string
#   'header'      arg = (name, sub)      -> response header <name> contains sub (case-insensitive)
#   'nodata_msg'  arg = substring        -> .message contains arg AND no 'data' key
#   'data_msg'    arg = substring        -> .message contains arg AND 'data' key present
# ---------------------------------------------------------------------------
SIGNALS = [
  # ======================= server/vendor-UNIQUE ===========================
  # Inigo gateway — always injects its own extensions block
  ('inigo', 'gateway', UNIQUE, 'typename', 'ext_key', 'inigo'),

  # Hasura (Haskell) — unmistakable root type name + owned error phrasing
  ('hasura', 'hasura', UNIQUE, 'cached_q', 'typename', 'query_root'),
  ('hasura', 'hasura', UNIQUE, 'badfield', 'msg', "not found in type: 'query_root'"),
  ('hasura', 'hasura', STRONG, 'skip_q',   'msg', 'directive "skip" is not allowed on a query'),
  ('hasura', 'hasura', STRONG, 'schema_nosel', 'msg', 'missing selection set for "__Schema"'),

  # WPGraphQL (WordPress / webonyx-php) — owned request + debug extensions
  ('wpgraphql', 'webonyx-php', UNIQUE, 'empty', 'msg',
   'GraphQL Request must include at least one of those two parameters: "query" or "queryId"'),
  ('wpgraphql', 'webonyx-php', UNIQUE, 'alias_dollar', 'ext_field',
   (('debug', 0, 'type'), 'DEBUG_LOGS_INACTIVE')),

  # Gato GraphQL / GraphQL API for WP (webonyx-php)
  ('graphql-api-for-wp', 'webonyx-php', STRONG, 'alias_dollar', 'alias', ('alias1$1', 'QueryRoot')),
  ('graphql-api-for-wp', 'webonyx-php', UNIQUE, 'unknown_dir_f', 'msg',
   'No DirectiveResolver resolves directive with name'),
  ('graphql-api-for-wp', 'webonyx-php', STRONG, 'skip_q', 'msg',
   "Argument 'if' cannot be empty, so directive 'skip' has been ignored"),
  ('graphql-api-for-wp', 'webonyx-php', STRONG, 'empty', 'msg', 'The query in the body is empty'),

  # AWS AppSync — MisplacedDirective error type
  ('aws-appsync', 'appsync', STRONG, 'skip_q', 'msg', 'MisplacedDirective'),

  # Absinthe (Elixir) — RootQueryType root name
  ('absinthe-graphql', 'absinthe', UNIQUE, 'badfield', 'msg',
   'Cannot query field "graphw00f" on type "RootQueryType".'),

  # Lacinia (Clojure) — backtick error style + QueryRoot
  ('lacinia', 'lacinia', UNIQUE, 'badfield', 'msg',
   "Cannot query field `graphw00f' on type `QueryRoot'."),

  # Sangria (Scala) — top-level syntaxError key
  ('sangria', 'sangria', UNIQUE, 'badkw', 'top',
   ('syntaxError', 'Syntax error while parsing GraphQL query. Invalid input "queryy"')),

  # Dgraph — owned no-schema message + Query root under @cascade
  ('dgraph', 'dgraph', UNIQUE, 'typename', 'msg',
   "Not resolving __typename. There's no GraphQL schema in Dgraph"),

  # Diana.jl (Julia)
  ('dianajl', 'dianajl', UNIQUE, 'badkw', 'msg',
   'Syntax Error GraphQL request (1:1) Unexpected Name "queryy"'),

  # Caliban (Scala)
  ('caliban', 'caliban', UNIQUE, 'frag_unused', 'msg', "Fragment 'woof' is not used in any spread"),

  # tartiflette (Python, libgraphqlparser) — "Unknow" typo + <>-bracket directive errors
  ('tartiflette', 'tartiflette', UNIQUE, 'unknown_dir_f', 'msg', 'is not used in a valid location'),
  ('tartiflette', 'tartiflette', UNIQUE, 'skip_q', 'msg', 'Missing mandatory argument < if > in directive < @skip >.'),
  ('tartiflette', 'tartiflette', UNIQUE, 'badkw', 'msg', 'syntax error, unexpected IDENTIFIER'),
  ('tartiflette', 'tartiflette', STRONG, 'badfield', 'msg', "doesn't exist on Query"),

  # pg_graphql (Supabase, Rust/Postgres)
  ('pg_graphql', 'pg_graphql', STRONG, 'skip_badarg', 'msg', 'Unknown argument to @skip: aa'),

  # graphql-dotnet (.NET) — server rewrites parse errors + unique 'number' (spec section) extension key
  ('graphql-dotnet', 'graphql-dotnet', STRONG, 'skip_q', 'msg', "Directive 'skip' may not be used on Query."),
  ('graphql-dotnet', 'graphql-dotnet', STRONG, 'badkw', 'msg', 'Error parsing query:'),
  ('graphql-dotnet', 'graphql-dotnet', STRONG, 'badkw', 'err_ext_present', ('number',)),

  # HotChocolate (.NET)
  ('hotchocolate', 'hotchocolate', STRONG, 'badkw', 'msg', 'Unexpected token: Name.'),
  ('hotchocolate', 'hotchocolate', STRONG, 'dup_dir', 'msg',
   'is not supported by the current schema.'),

  # graphql-ruby — owned directive-on-query phrasing + Parse error style
  ('ruby-graphql', 'graphql-ruby', STRONG, 'skip_q', 'msg',
   "'@skip' can't be applied to queries (allowed: fields, fragment spreads, inline fragments)"),
  ('ruby-graphql', 'graphql-ruby', STRONG, 'deprecated_q', 'msg',
   "'@deprecated' can't be applied to queries"),
  ('ruby-graphql', 'graphql-ruby', FAMILY, 'curly', 'msg', 'Parse error on "}" (RCURLY)'),

  # HyperGraphQL (Java)
  ('hypergraphql', 'hypergraphql', STRONG, 'badkw', 'msg',
   'Validation error of type InvalidSyntax: Invalid query syntax.'),
  ('hypergraphql', 'hypergraphql', STRONG, 'deprecated_f', 'msg',
   'Validation error of type UnknownDirective: Unknown directive deprecated'),

  # Agoo (Ruby, C)
  ('agoo', 'agoo', STRONG, 'badfield', 'part', ('code', 'eval error')),

  # Mercurius (Fastify/JS) — server-owned "Unknown query" on empty
  ('mercurius', 'graphql-js', STRONG, 'empty', 'msg', 'Unknown query'),

  # async-graphql (Rust, pest parser) — dominant Rust server; 'queryy' PARSES OK here (pest matches
  # the 'query' prefix), so the reliable probe is a bare garbage token ('aaa'). tailcall shares the
  # async-graphql-parser, so this string also covers tailcall (flagged as async-graphql-parser family).
  ('async-graphql', 'async-graphql', STRONG, 'aaa', 'msg', 'expected executable_definition'),
  ('async-graphql', 'async-graphql', STRONG, 'aaa', 'msg', ' --> 1:1'),

  # jaal (Go)
  ('jaal', 'jaal', STRONG, 'empty', 'msg', 'must have a single query'),

  # morpheus-graphql (Haskell)
  ('morpheus-graphql', 'morpheus', STRONG, 'badkw', 'msg', 'expecting white space'),

  # Directus (TS, graphql-js) — vendor error code
  ('directus', 'graphql-js', STRONG, 'empty', 'ext_code', 'INVALID_PAYLOAD'),

  # ---- JS servers on top of graphql-js (server-layer tells, NOT parser strings) ----
  # Apollo Server (v3/4/5): Automatic Persisted Queries (default-on) + branded landing page.
  ('apollo', 'graphql-js', STRONG, 'apq', 'msg', 'PersistedQueryNotFound'),
  ('apollo', 'graphql-js', STRONG, 'apq', 'msg', 'PersistedQueryNotSupported'),
  ('apollo', 'graphql-js', STRONG, 'apq', 'ext_code', 'PERSISTED_QUERY_NOT_FOUND'),
  ('apollo', 'graphql-js', STRONG, 'noquery', 'msg', 'GraphQL operations must contain a non-empty'),
  ('apollo', 'graphql-js', UNIQUE, 'landing', 'html', '<title>Apollo Server</title>'),
  ('apollo', 'graphql-js', UNIQUE, 'landing', 'html', 'Apollo server landing page'),

  # Apollo Router (Rust federation gateway) — distinct codes ("PARSING" not "PARSE") + landing.
  ('apollo-router', 'apollo-router', UNIQUE, 'noquery', 'ext_code', 'MISSING_QUERY_STRING'),
  ('apollo-router', 'apollo-router', UNIQUE, 'badkw', 'ext_code', 'GRAPHQL_PARSING_FAILED'),
  ('apollo-router', 'apollo-router', UNIQUE, 'landing', 'html', 'Welcome to the Apollo Router'),
  ('apollo-router', 'apollo-router', STRONG, 'landing', 'html', '<title>Apollo Router</title>'),

  # GraphQL Yoga (The Guild) — rejects unknown body params (unique), branded landing/IDE.
  ('graphql_yoga', 'graphql-js', STRONG, 'extra_param', 'msg', 'Unexpected parameter'),
  ('graphql_yoga', 'graphql-js', STRONG, 'query_int', 'msg', 'Expected "query" param to be a string'),
  ('graphql_yoga', 'graphql-js', UNIQUE, 'landing', 'html', 'Welcome to GraphQL Yoga'),
  ('graphql_yoga', 'graphql-js', UNIQUE, 'landing', 'html', 'YogaGraphiQL'),
  ('graphql_yoga', 'graphql-js', STRONG, 'subscription', 'msg',
   'asyncExecutionResult[Symbol.asyncIterator] is not a function'),  # v1/v2 legacy tell

  # express-graphql — unique GraphiQL comment; "Must provide query string." (no code) is the body tell.
  ('express-graphql', 'graphql-js', UNIQUE, 'landing', 'html', 'add "&raw" to the end of the URL'),
  ('express-graphql', 'graphql-js', STRONG, 'noquery', 'msg', 'Must provide query string.'),

  # graphql-http (spec reference server) — terse messages, no extensions.code, no landing/IDE.
  ('graphql-http', 'graphql-http', STRONG, 'noquery', 'msg', 'Missing query'),
  ('graphql-http', 'graphql-http', STRONG, 'query_int', 'msg', 'Invalid query'),

  # ======================= response-header tells (always-on, high precision) ====
  ('directus', 'graphql-js', UNIQUE, 'typename', 'header', ('x-powered-by', 'Directus')),
  ('dgraph', 'dgraph', UNIQUE, 'typename', 'header', ('graphql-toucheduids', '')),
  ('wpgraphql', 'webonyx-php', STRONG, 'typename', 'header', ('x-graphql-url', '')),
  ('inigo', 'gateway', UNIQUE, 'typename', 'header', ('inigo-router-traceid', '')),
  ('postgraphile', 'postgraphile', UNIQUE, 'typename', 'header', ('x-graphql-event-stream', '')),

  # ======================= federation gateways / routers (new engines) ==========
  # WunderGraph Cosmo Router (Go) — default playground title
  ('cosmo-router', 'cosmo-router', UNIQUE, 'landing', 'html', '<title>WunderGraph Playground</title>'),
  ('cosmo-router', 'cosmo-router', STRONG, 'badfield', 'ext_code', 'BATCHING_SUBSCRIPTION_UNSUPPORTED'),

  # Hive Gateway (The Guild, Yoga-based) — hardcoded landing string (survives productName override)
  ('hive-gateway', 'graphql-js', UNIQUE, 'landing', 'html', 'you need to configure Hive Gateway.'),
  ('hive-gateway', 'graphql-js', STRONG, 'landing', 'html', 'Welcome to Hive Gateway'),

  # PostGraphile (Node, graphql-js) — Ruru IDE title (Graphile-exclusive brand)
  ('postgraphile', 'postgraphile', UNIQUE, 'landing', 'html', 'Ruru - GraphQL/Grafast IDE'),

  # Saleor (Python/Graphene e-commerce) — always-on query-cost extension
  ('saleor', 'graphql-core', UNIQUE, 'typename', 'ext_present', ('cost', 'maximumAvailable')),
  ('saleor', 'graphql-core', STRONG, 'typename', 'ext_present', ('cost', 'requestedQueryCost')),

  # Grafbase (Rust edge gateway) — SCREAMING_SNAKE OPERATION_* codes + grafbase extension block
  ('grafbase', 'grafbase', STRONG, 'badfield', 'ext_code', 'OPERATION_VALIDATION_ERROR'),
  ('grafbase', 'grafbase', UNIQUE, 'typename', 'ext_present', ('grafbase', 'traceId')),

  # Generic Apollo Federation SUBGRAPH — _service{sdl} returns the SDL string. Marks a federated
  # subgraph (apollo-server+@apollo/subgraph, Saleor, graphql-java federation, Cosmo/Hive subgraphs).
  ('apollo-federation', 'federation', STRONG, 'federation', 'federation', None),

  # ======================= parser-dialect FAMILY signals ===================
  # graphql-java family (graphql-java, Netflix DGS, Spring-GraphQL).
  # Current wording (>=v17ish): "Invalid syntax with offending token 'queryy' at line 1 column 1";
  # legacy wording: "Invalid Syntax : offending token 'queryy'". Keep both.
  ('graphql-java', 'graphql-java', FAMILY, 'badkw', 'msg', "Invalid syntax with offending token 'queryy'"),
  ('graphql-java', 'graphql-java', FAMILY, 'badkw', 'msg', "Invalid Syntax : offending token 'queryy'"),
  ('graphql-java', 'graphql-java', FAMILY, 'badkw', 'err_ext_present', ('classification',)),
  ('graphql-java', 'graphql-java', STRONG, 'dup_dir', 'msg',
   'Validation error of type DuplicateDirectiveName: Directives must be uniquely named within a location.'),
  ('graphql-java', 'graphql-java', FAMILY, 'empty', 'msg', "Invalid Syntax : offending token '<EOF>'"),

  # Netflix DGS (graphql-java + default GraphQLJavaErrorInstrumentation) — adds errorType/errorDetail
  # extension keys on top of graphql-java. Spring-for-GraphQL is wire-indistinguishable from bare
  # graphql-java on syntax/validation probes (report graphql-java).
  ('graphql-dgs', 'graphql-java', STRONG, 'badfield', 'err_ext_present', ('errorType',)),
  ('graphql-dgs', 'graphql-java', STRONG, 'badkw', 'err_ext_present', ('errorType',)),

  # gqlgen (Go, gqlparser)
  ('gqlgen', 'gqlgen', STRONG, 'curly', 'msg', 'expected at least one definition'),
  ('gqlgen', 'gqlgen', STRONG, 'badkw', 'msg', 'Expected Name, found <Invalid>'),

  # graphql-go (Go) — RootQuery root name is the reliable tell ("Must provide an operation."
  # is SHARED with graphql-js/graphql-core and must NOT be used alone).
  ('graphql-go', 'graphql-go', STRONG, 'typename', 'typename', 'RootQuery'),
  ('graphql-go', 'graphql-go', FAMILY, 'curly', 'msg', 'Unexpected empty IN'),

  # juniper (Rust)
  ('juniper', 'juniper', STRONG, 'badkw', 'msg', 'Unexpected "queryy"'),

  # graphene 2 (Python, graphql-core v2) — legacy "Syntax Error GraphQL (L:C)" prefix
  ('graphene', 'graphql-core-legacy', STRONG, 'aaa', 'msg', 'Syntax Error GraphQL (1:1)'),

  # graphql-php / webonyx (base for wpgraphql/lighthouse/gato) — quoted QUERY + unexpected char
  ('graphql-php', 'webonyx-php', FAMILY, 'bang', 'msg',
   'Syntax Error: Cannot parse the unexpected character'),
  ('graphql-php', 'webonyx-php', STRONG, 'deprecated_q', 'msg',
   'Directive "deprecated" may not be used on "QUERY".'),

  # Lighthouse (PHP/Laravel, webonyx) — @include(if: bad) -> internal error category
  ('lighthouse', 'webonyx-php', WEAK, 'incl_bad', 'part', ('category', 'internal')),

  # Strawberry (Python, graphql-core) — branded IDE, own no-query msg, always-present data key
  ('strawberry', 'graphql-core', UNIQUE, 'landing', 'html', '<title>Strawberry GraphiQL</title>'),
  ('strawberry', 'graphql-core', STRONG, 'noquery', 'msg', 'No GraphQL query found in the request'),
  ('strawberry', 'graphql-core', STRONG, 'deprecated_q', 'data_msg',
   "Directive '@deprecated' may not be used on query."),

  # Ariadne (Python, graphql-core) — own HTTP-layer validation ("must be a string") + data-less envelope
  ('ariadne', 'graphql-core', STRONG, 'query_int', 'msg', 'The query must be a string.'),
  ('ariadne', 'graphql-core', STRONG, 'noquery', 'msg', 'The query must be a string.'),
  ('ariadne', 'graphql-core', FAMILY, 'unknown_dir_f', 'nodata_msg', "Unknown directive '@graphw00f'."),

  # ballerina — self-referential fragment phrasing (graphql-js-like but ballerina-owned wording kept)
  ('ballerina', 'ballerina', STRONG, 'frag_cycle', 'msg', 'Cannot spread fragment "A" within itself via "B"'),

  # ---- graphql-js reference family (shared strings) -----------------------
  # These identify the LIBRARY, not the server. They upgrade to a specific
  # engine only via the server-unique signals above / added below.
  ('graphql-js', 'graphql-js', FAMILY, 'skip_q', 'msg',
   'Directive "@skip" argument "if" of type "Boolean!" is required, but it was not provided.'),
  ('graphql-js', 'graphql-js', FAMILY, 'skip_q', 'msg',
   'Argument "@skip(if:)" of type "Boolean!" is required, but it was not provided.'),
  ('graphql-js', 'graphql-js', FAMILY, 'deprecated_q', 'msg',
   'Directive "@deprecated" may not be used on QUERY.'),
  # JS-vs-Python parser dialect: graphql-js double-quotes the offending token.
  ('graphql-js', 'graphql-js', FAMILY, 'badkw', 'msg', 'Syntax Error: Unexpected Name "queryy".'),

  # ---- graphql-core reference family (Python: ariadne/strawberry/graphene3)
  ('graphql-core', 'graphql-core', FAMILY, 'deprecated_q', 'msg',
   "Directive '@deprecated' may not be used on QUERY."),
  ('graphql-core', 'graphql-core', FAMILY, 'unknown_dir_f', 'msg', "Unknown directive '@graphw00f'."),
  # graphql-core single-quotes the offending token (splits Python family from graphql-js).
  ('graphql-core', 'graphql-core', FAMILY, 'badkw', 'msg', "Syntax Error: Unexpected Name 'queryy'."),
]

# Engines that ARE their own family label when only family-level evidence exists.
# (When we can only resolve the family, map it to a representative engine id or a
#  generic family id that main.py can render.)
FAMILY_FALLBACK = {
  'graphql-js':          'graphql-js',
  'graphql-core':        'graphql-core',
  'graphql-core-legacy': 'graphene',
  'webonyx-php':         'graphql-php',
  'graphql-java':        'graphql-java',
  'graphql-go':          'graphql-go',
  'gqlgen':              'gqlgen',
  'graphql-ruby':        'ruby-graphql',
  'hasura':              'hasura',
  'async-graphql':       'async-graphql',
  'postgraphile':        'postgraphile',
  'grafbase':            'grafbase',
  'cosmo-router':        'cosmo-router',
  'apollo-router':       'apollo-router',
  'federation':          'apollo-federation',
}
