import requests

from graphw00f.helpers import error_contains

requests.packages.urllib3.disable_warnings()

class GraphQLDetectionFailed(Exception):
  pass

class GraphQLError(Exception):
  pass

class GRAPHW00F:
  def __init__(self, headers,
                     cookies,
                     timeout,
                     proxies,
                     follow_redirects=False):
    self.url = 'http://example.com'
    self.cookies = cookies
    self.headers = headers
    self.follow_redirects = follow_redirects,
    self.timeout = timeout
    self.proxies = proxies

  def check(self, url):
    query = '''
      query {
        __typename
      }
    '''
    response = self.graph_query(url, payload=query)

    if response.get('data'):
      if response.get('data', {}).get('__typename', '') in ('Query', 'QueryRoot', 'query_root'):
        return True
    elif response.get('errors') and (any('locations' in i for i in response['errors']) or any('extensions' in i for i in response['errors'])):
      return True
    elif response.get('data'):
      return True
    else:
      raise GraphQLDetectionFailed

  def execute(self, url):
    self.url = url
    if self.engine_lighthouse():
      return 'lighthouse'
    elif self.engine_caliban():
      return 'caliban'
    elif self.engine_lacinia():
      return 'lacinia'
    elif self.engine_jaal():
      return 'jaal'
    elif self.engine_morpheus():
      return 'morpheus-graphql'
    elif self.engine_mercurius():
      return 'mercurius'
    elif self.engine_graphql_yoga():
      return 'graphql_yoga'
    elif self.engine_agoo():
      return 'agoo'
    elif self.engine_tailcall():
      return 'tailcall'
    elif self.engine_dgraph():
      return 'dgraph'
    elif self.engine_graphene():
      return 'graphene'
    elif self.engine_ariadne():
      return 'ariadne'
    elif self.engine_apollo():
      return 'apollo'
    elif self.engine_awsappsync():
      return 'aws-appsync'
    elif self.engine_hasura():
      return 'hasura'
    elif self.engine_wpgraphql():
      return 'wpgraphql'
    elif self.engine_graphqlapiforwp():
      return 'graphql-api-for-wp'
    elif self.engine_graphqljava():
      return 'graphql-java'
    elif self.engine_hypergraphql():
      return 'hypergraphql'
    elif self.engine_ruby():
      return 'ruby-graphql'
    elif self.engine_graphqlphp():
      return 'graphql-php'
    elif self.engine_gqlgen():
      return 'gqlgen'
    elif self.engine_graphqlgo():
      return 'graphql-go'
    elif self.engine_juniper():
      return 'juniper'
    elif self.engine_sangria():
      return 'sangria'
    elif self.engine_flutter():
      return 'flutter'
    elif self.engine_dianajl():
      return 'dianajl'
    elif self.engine_strawberry():
      return 'strawberry'
    elif self.engine_tartiflette():
      return 'tartiflette'
    elif self.engine_directus():
      return 'directus'
    elif self.engine_absinthe():
      return 'absinthe-graphql'
    elif self.engine_graphqldotnet():
      return 'graphql-dotnet'
    elif self.engine_pggraphql():
      return 'pg_graphql'

    return None

  def graph_query(self, url, operation='query', payload={}):
    try:
      response = requests.post(url,
                             headers=self.headers,
                             cookies=self.cookies,
                             verify=False,
                             allow_redirects=self.follow_redirects,
                             timeout=self.timeout,
                             proxies=self.proxies,
                             json={operation:payload})
      return response.json()
    except:
      return {}

  def engine_graphql_yoga(self):
    query = '''
      subscription {
         __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'asyncExecutionResult[Symbol.asyncIterator] is not a function') or error_contains(response, 'Unexpected error.'):
        return True

    return False
  def engine_apollo(self):
    query = '''
      query @skip {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive "@skip" argument "if" of type "Boolean!" is required, but it was not provided.'):
      return True

    query = '''
      query @deprecated {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive "@deprecated" may not be used on QUERY.'):
      return True

    return False

  def engine_awsappsync(self):
      query = 'query @skip { __typename }'
      response = self.graph_query(self.url, payload=query)
      return error_contains(response, 'MisplacedDirective')

  def engine_graphene(self):
    query = '''aaa'''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Syntax Error GraphQL (1:1)'):
      return True

    return False

  def engine_hasura(self):
    query = '''
      query @cached {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if response.get('data'):
      if response.get('data', {}).get('__typename', '') == 'query_root':
        return True
    query = '''
     query {
       aaa
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'field "aaa" not found in type: \'query_root\''):
      return True

    query = '''
      query @skip {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'directive "skip" is not allowed on a query'):
      return True

    query = '''
      query {
        __schema
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'missing selection set for "__Schema"'):
      return True

    return False

  def engine_graphqlphp(self):
    query = '''
      query ! {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Syntax Error: Cannot parse the unexpected character "?".'):
      return True

    query = '''
      query @deprecated {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive "deprecated" may not be used on "QUERY".'):
      return True

    return False

  def engine_ruby(self):
    query = '''
     query @skip {
       __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, '\'@skip\' can\'t be applied to queries (allowed: fields, fragment spreads, inline fragments)'):
      return True
    elif error_contains(response, 'Directive \'skip\' is missing required arguments: if'):
      return True

    query = '''
     query @deprecated {
       __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, '\'@deprecated\' can\'t be applied to queries'):
      return True

    query = '''
      query {
       __typename {
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Parse error on "}" (RCURLY)'):
      return True

    query = '''
      query {
        __typename @skip
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive \'skip\' is missing required arguments: if'):
      return True

    return False

  def engine_hypergraphql(self):
    query = '''
     zzz {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Validation error of type InvalidSyntax: Invalid query syntax.'):
      return True

    query = '''
      query {
        alias1:__typename @deprecated
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Validation error of type UnknownDirective: Unknown directive deprecated @ \'__typename\''):
      return True

    return False

  def engine_graphqljava(self):
    query = '''
     queryy  {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Invalid Syntax : offending token \'queryy\''):
      return True

    query = '''
     query @aaa@aaa {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Validation error of type DuplicateDirectiveName: Directives must be uniquely named within a location.'):
      return True

    query = ''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Invalid Syntax : offending token \'<EOF>\''):
      return True

    return False

  def engine_ariadne(self):
    query = '''
      query {
        __typename @abc
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Unknown directive \'@abc\'.') and 'data' not in response:
      return True

    query = ''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'The query must be a string.'):
      return True

    return False

  def engine_graphqlapiforwp(self):
    query = '''
     query {
       alias1$1:__typename
     }
    '''
    response = self.graph_query(self.url, payload=query)
    if response.get('data'):
      if response.get('data', {}).get('alias1$1', '') == 'QueryRoot':
        return True

    query = '''query aa#aa { __typename }'''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Unexpected token "END"'):
      return True

    query = '''
      query @skip {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Argument \'if\' cannot be empty, so directive \'skip\' has been ignored'):
      return True

    query = '''
      query @doesnotexist {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'No DirectiveResolver resolves directive with name \'doesnotexist\''):
      return True

    query = ''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'The query in the body is empty'):
      return True

    return False

  def engine_wpgraphql(self):
    query = ''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'GraphQL Request must include at least one of those two parameters: "query" or "queryId"'):
      return True

    query = '''
     query {
       alias1$1:__typename
     }
    '''
    response = self.graph_query(self.url, payload=query)
    if not error_contains(response, 'Syntax Error: Expected Name, found $'):
      return False

    try:
      debug_msg = response['extensions']['debug'][0]
      if debug_msg['type'] == 'DEBUG_LOGS_INACTIVE' or \
        debug_msg['message'] == 'GraphQL Debug logging is not active. To see debug logs, GRAPHQL_DEBUG must be enabled.':
        return True
    except KeyError:
      pass

    return False

  def engine_gqlgen(self):
    query = '''
      query  {
      __typename {
    }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'expected at least one definition'):
      return True

    query = '''
      query  {
      alias^_:__typename {
    }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Expected Name, found <Invalid>'):
      return True

    return False

  def engine_graphqlgo(self):
    query = '''
      query {
      __typename {
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Unexpected empty IN'):
      return True

    query = ''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Must provide an operation.'):
      return True

    query = '''
      query {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    try:
      if response['data'] != None and response['data']['__typename'] == 'RootQuery':
        return True
    except KeyError:
      pass

    return False

  def engine_juniper(self):
    query = '''
      queryy {
        __typename
    }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Unexpected "queryy"'):
      return True

    query = ''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Unexpected end of input'):
      return True

    return False

  def engine_sangria(self):
    query = '''
      queryy {
        __typename
    }
    '''
    response = self.graph_query(self.url, payload=query)
    syntaxError = response.get('syntaxError', '')
    if 'Syntax error while parsing GraphQL query. Invalid input "queryy", expected ExecutableDefinition or TypeSystemDefinition' in syntaxError:
      return True

    return False

  def engine_flutter(self):
    query = '''
      query {
        __typename @deprecated
    }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive "deprecated" may not be used on FIELD.'):
      return True

    return False

  def engine_dianajl(self):
    query = '''queryy { __typename }'''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Syntax Error GraphQL request (1:1) Unexpected Name "queryy"'):
      return True

    return False

  def engine_strawberry(self):
    query = '''
      query @deprecated {
        __typename
      }'''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive \'@deprecated\' may not be used on query.') and 'data' in response:
      return True

    return False

  def engine_tartiflette(self):
    query = '''
      query @a { __typename }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Unknow Directive < @a >.'):
      return True

    query = '''
      query @skip { __typename }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Missing mandatory argument < if > in directive < @skip >.'):
      return True

    query = '''
      query { graphwoof }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Field graphwoof doesn\'t exist on Query'):
      return True

    query = '''
      query {
        __typename @deprecated
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive < @deprecated > is not used in a valid location.'):
      return True

    query = '''
      queryy {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'syntax error, unexpected IDENTIFIER'):
      return True

    return False

  def engine_tailcall(self):
    query = '''
      aa {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'expected executable_definition'):
      return True

    return False


  def engine_dgraph(self):
    query = '''
      query {
        __typename @cascade
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if 'data' in response and response['data']:
      if response.get('data').get('__typename', '') == 'Query':
        return True

    query = '''
      query {
        __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Not resolving __typename. There\'s no GraphQL schema in Dgraph. Use the /admin API to add a GraphQL schema'):
      return True

    return False

  def engine_directus(self):
    query = ''

    response = self.graph_query(self.url, payload=query)
    errors = response.get('errors', [])
    if response.get('errors', []):
      if errors and errors[0].get('extensions', {}).get('code' '') == 'INVALID_PAYLOAD':
        return True

    return False

  def engine_lighthouse(self):
    query = '''
      query {
        __typename @include(if: falsee)
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Internal server error') or error_contains(response, 'internal', part='category'):
      return True

    return False

  def engine_agoo(self):
    query = '''
      query {
        zzz
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'eval error', part='code'):
      return True

    return False

  def engine_mercurius(self):
    query = ''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Unknown query'):
      return True
    return False

  def engine_morpheus(self):
    query = '''
      queryy {
          __typename
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'expecting white space') or error_contains(response, 'offset'):
      return True

    return False

  def engine_lacinia(self):
    query = '''
      query {
        graphw00f
      }
    '''

    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Cannot query field `graphw00f\' on type `QueryRoot\'.'):
        return True

    return False

  def engine_jaal(self):
    query = '''{}'''
    response = self.graph_query(self.url, payload=query, operation='{}')

    if error_contains(response, 'must have a single query') or error_contains(response, 'offset'):
      return True

    return False

  def engine_caliban(self):
    query = '''
      query {
        __typename
      }

      fragment woof on __Schema {
        directives {
          name
        }
      }
    '''

    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Fragment \'woof\' is not used in any spread'):
      return True

    return False

  def engine_absinthe(self):
    query = '''
      query {
        graphw00f
      }
    '''

    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'Cannot query field \"graphw00f\" on type \"RootQueryType\".'):
        return True

    return False

  def engine_graphqldotnet(self):
    query = 'query @skip { __typename }'
    response = self.graph_query(self.url, payload=query)
    return error_contains(response, 'Directive \'skip\' may not be used on Query.')
  
  def engine_pggraphql(self):
    query = '''query { __typename @skip(aa:true) }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Unknown argument to @skip: aa'):
      return True
    
    return False