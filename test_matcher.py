#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit test for the precision matcher — proves scoring + no over-claim."""
import sys
sys.path.insert(0, '.')
from graphw00f.lib import GRAPHW00F

g = GRAPHW00F(headers={}, cookies={}, timeout=5, proxies=None)

def E(msg):          # error response with a single message
  return {'errors': [{'message': msg}]}
def Edata(msg):      # validation error but WITH a data key (strawberry tell)
  return {'data': None, 'errors': [{'message': msg}]}
def D(**data):       # data response
  return {'data': data}

CASES = [
  # name, responses(dict by probe id), expected_engine, expected_confidence
  ('hasura (query_root)',
     {'cached_q': D(__typename='query_root')}, 'hasura', 'high'),

  ('graphql-js generic (only family strings — must NOT be apollo/graphql-go)',
     {'skip_q': E('Argument "@skip(if:)" of type "Boolean!" is required, but it was not provided.'),
      'deprecated_q': E('Directive "@deprecated" may not be used on QUERY.')},
     'graphql-js', 'low'),

  ('OLD graphql-go false-positive trap ("Must provide an operation." + js family)',
     {'empty': E('Must provide an operation.'),
      'skip_q': E('Argument "@skip(if:)" of type "Boolean!" is required, but it was not provided.')},
     'graphql-js', 'low'),

  ('graphql-go REAL (RootQuery root name)',
     {'typename': D(__typename='RootQuery')}, 'graphql-go', 'medium'),

  ('tartiflette (own parser + <>-directive)',
     {'badkw': E('syntax error, unexpected IDENTIFIER'),
      'skip_q': E('Missing mandatory argument < if > in directive < @skip >.')},
     'tartiflette', 'high'),

  ('absinthe (RootQueryType)',
     {'badfield': E('Cannot query field "graphw00f" on type "RootQueryType".')},
     'absinthe-graphql', 'high'),

  ('graphql-java (offending token)',
     {'badkw': E("Invalid Syntax : offending token 'queryy' at line 1"),
      'dup_dir': E('Validation error of type DuplicateDirectiveName: Directives must be uniquely named within a location.')},
     'graphql-java', 'medium'),

  ('gqlgen (gqlparser)',
     {'curly': E('expected at least one definition'),
      'badkw': E('Expected Name, found <Invalid>')},
     'gqlgen', 'medium'),

  ('inigo gateway (extensions.inigo)',
     {'typename': {'data': {'__typename': 'Query'}, 'extensions': {'inigo': {'trace': 'x'}}}},
     'inigo', 'high'),

  ('graphene 2 (legacy core prefix)',
     {'aaa': E('Syntax Error GraphQL (1:1) Unexpected Name "aaa"')},
     'graphene', 'medium'),

  ('wpgraphql (owned request error)',
     {'empty': E('GraphQL Request must include at least one of those two parameters: "query" or "queryId"')},
     'wpgraphql', 'high'),

  ('pg_graphql (unknown arg to @skip)',
     {'skip_badarg': E('Unknown argument to @skip: aa')},
     'pg_graphql', 'medium'),

  ('ariadne (non-string query -> own wrapper msg)',
     {'query_int': E('The query must be a string.')}, 'ariadne', 'medium'),

  ('strawberry (branded GraphiQL landing)',
     {'landing': {'__html__': '<!DOCTYPE html><html><head><title>Strawberry GraphiQL</title></head></html>'}},
     'strawberry', 'high'),

  ('strawberry vs ariadne split (data key present + no-query msg)',
     {'noquery': E('No GraphQL query found in the request'),
      'deprecated_q': Edata("Directive '@deprecated' may not be used on query.")},
     'strawberry', 'medium'),

  ('graphql-core generic v3 (single-quote token, no unique tell — NOT graphql-js)',
     {'badkw': E("Syntax Error: Unexpected Name 'queryy'.")}, 'graphql-core', 'low'),

  ('graphql-js vs graphql-core dialect (double-quote token -> js)',
     {'badkw': E('Syntax Error: Unexpected Name "queryy".')}, 'graphql-js', 'low'),

  # ---- JS server layer (all sit on graphql-js; server tells must decide) ----
  ('apollo server (APQ default-on, no landing page — like a real prod API)',
     {'apq': {'errors': [{'message': 'PersistedQueryNotFound',
                          'extensions': {'code': 'PERSISTED_QUERY_NOT_FOUND'}}]}},
     'apollo', 'medium'),

  ('apollo server (branded landing page)',
     {'landing': {'__html__': '<html><head><title>Apollo Server</title>'
                  '<meta name="description" content="Apollo server landing page"></head></html>'}},
     'apollo', 'high'),

  ('apollo ROUTER (distinct codes) — must NOT be apollo server or express-graphql',
     {'noquery': {'errors': [{'message': 'Must provide query string.',
                              'extensions': {'code': 'MISSING_QUERY_STRING'}}]},
      'badkw': {'errors': [{'message': 'parsing error', 'extensions': {'code': 'GRAPHQL_PARSING_FAILED'}}]}},
     'apollo-router', 'high'),

  ('graphql yoga (rejects unknown body param) — must NOT be apollo despite shared codes',
     {'extra_param': E('Unexpected parameter "graphw00f" in the request body.'),
      'landing': {'__html__': '<title>Welcome to GraphQL Yoga</title>'}},
     'graphql_yoga', 'high'),

  ('express-graphql (unique GraphiQL &raw comment)',
     {'landing': {'__html__': '<!-- ... add "&raw" to the end of the URL within a browser. -->'},
      'noquery': E('Must provide query string.')},
     'express-graphql', 'high'),

  ('graphql-http (terse, no code, no landing)',
     {'noquery': E('Missing query'), 'query_int': E('Invalid query')},
     'graphql-http', 'medium'),

  # ---- vendor / gateway / federation (new engines) ----
  ('apollo federation subgraph (_service.sdl)',
     {'federation': {'data': {'_service': {'sdl': 'type Query { hi: String }'}}}},
     'apollo-federation', 'medium'),

  ('async-graphql (pest parser)',
     {'aaa': E(' --> 1:1\n  |\n1 | aaa\n  | ^---\n  = expected executable_definition')},
     'async-graphql', 'medium'),

  ('saleor (always-on cost extension)',
     {'typename': {'data': {'__typename': 'Query'},
                   'extensions': {'cost': {'requestedQueryCost': 0, 'maximumAvailable': 50000}}}},
     'saleor', 'high'),

  ('netflix dgs (errorType extension over graphql-java)',
     {'badfield': {'errors': [{'message': "Field 'graphw00f' in type 'Query' is undefined",
                               'extensions': {'errorType': 'BAD_REQUEST', 'classification': 'ValidationError'}}]}},
     'graphql-dgs', 'medium'),

  ('cosmo router (WunderGraph Playground landing)',
     {'landing': {'__html__': '<html><head><title>WunderGraph Playground</title></head></html>'}},
     'cosmo-router', 'high'),

  ('directus via X-Powered-By header',
     {'typename': D(__typename='Query')}, 'directus', 'high',
     {'typename': {'X-Powered-By': 'Directus'}}),

  ('dgraph via Graphql-TouchedUids header',
     {'typename': D(__typename='Query')}, 'dgraph', 'high',
     {'typename': {'Graphql-TouchedUids': '42'}}),

  ('nothing matches -> None',
     {'typename': D(__typename='Query')}, None, None),
]

passed = 0
for case in CASES:
  name, responses, exp_engine, exp_conf = case[0], case[1], case[2], case[3]
  custom_headers = case[4] if len(case) > 4 else {}
  headers = {pid: {} for pid in responses}
  headers.update(custom_headers)
  res = g.detect_engine('http://x', responses=responses, headers=headers)
  got_engine = res['engine'] if res else None
  got_conf = res['confidence'] if res else None
  ok = (got_engine == exp_engine) and (exp_conf is None or got_conf == exp_conf)
  passed += ok
  flag = 'PASS' if ok else 'FAIL'
  extra = ''
  if res:
    cand = ', '.join('{}={}'.format(e, s) for e, s in res['candidates'][:4])
    extra = '  [{}conf={} cands: {}]'.format('AMBIG ' if res['ambiguous'] else '', got_conf, cand)
  print('[{}] {}\n        -> engine={} (exp {}){}'.format(flag, name, got_engine, exp_engine, extra))

print('\n{}/{} passed'.format(passed, len(CASES)))
sys.exit(0 if passed == len(CASES) else 1)
