import requests

from graphw00f.helpers import error_contains

requests.packages.urllib3.disable_warnings()

class GraphQLDetectionFailed(Exception):
  pass

class GraphQLUnknownState(Exception):
  pass

class GraphQLError(Exception):
  pass

class GRAPHW00F:
  def __init__(self, headers,
                     cookies,
                     follow_redirects=False):
    self.url = 'http://example.com'
    self.cookies = cookies
    self.headers = headers
    self.follow_redirects = follow_redirects
  
  def check(self, url):
    query = '''
      query {
        __typename
      }
    '''
    response = self.graph_query(url, payload=query)
    if response.get('data', {}).get('__typename', '') in ('Query', 'QueryRoot', 'query_root'):
      return True
    elif response.get('errors') and any('locations' in i for i in response['errors']):
      return True
    elif response.get('data'):
      return True
    else: 
      raise GraphQLDetectionFailed
    raise GraphQLUnknownState

  def execute(self, url):    
    self.url = url
    if self.engine_graphene():
      return 'graphene'
    elif self.engine_ariadne():
      return 'ariadne'
    elif self.engine_apollo():
      return 'apollo'
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
    return None
  
  def graph_query(self, url, operation='query', payload={}):
    try:
      response = requests.post(url, 
                             headers=self.headers,
                             cookies=self.cookies,
                             verify=False,
                             allow_redirects=self.follow_redirects,
                             json={operation:payload})
      return response.json()
    except GraphQLError:
      return {}
    except:
      return {}

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
        __schema 
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if error_contains(response, 'missing selection set for "__Schema"'):
      return True

    query = '''
     query { 
       aa 
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
      subscription {
        s 
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Schema is not configured for subscriptions.'):
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
     query aa@aa {
       __schema {
           directives {
             description
           }
        }
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive @aa is not defined'):
      return True
    
    query = '''
      query { 
        __schema 
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Field must have selections (field \'__schema\' returns __Schema but has no selections.'):
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
      __schema {
        directives {
          descriptio
        }
      }
    }
    '''
    response = self.graph_query(self.url, payload=query)
    if response.get('errors'):
      for i in response['errors']:
        qp = i.get('queryPath', [])
        matches = ['__schema', 'directives', 'descriptio'] 
        if qp == matches:
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
        __schema 
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Field \'__schema\' of type \'__Schema!\' must have a selection of subfields.'):
      return True
    
    query = '''
      subscription {
        s
      }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Could not connect to websocket endpoint'):
      return True
    
    query = ''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'The query must be a string.'):
      return True
        
    return False
  
  def engine_graphqlapiforwp(self):
    query = ''' 
     query {
       alias1$1:__schema
     }
    '''
    response = self.graph_query(self.url, payload=query)
    if response.get('data'):
      if response.get('data').get('alias1$1', '') == 'schema':
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
       alias1$1:__schema
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
      query @aa@aa  {
      __schema 
    }
    '''
    response = self.graph_query(self.url, payload=query)
    
    if error_contains(response, 'The directive "aa" can only be used once at this location.'):
      return True

  def engine_graphqlgo(self):
    query = ''' 
     query @skip {
       abc
     }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive "skip" may not be used on QUERY. Directive "@skip" argument "if" of type "Boolean!" is required but not provided'):
      return True
    
    query = ''
    response = self.graph_query(self.url, payload=query)
    
    if error_contains(response, 'Must provide an operation.'):
      return True

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
      queryy {
        __typename @deprecated
    }
    '''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'Directive "deprecated" may not be used on FIELD.'):
      return True
    
    return False

  def engine_dianajl(self):
    query = '''query a# { __typename }'''
    response = self.graph_query(self.url, payload=query)
    if error_contains(response, 'found EOF'):
      return True
    
    return False
