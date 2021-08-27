import requests

class GraphQLNotFound(Exception):
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
      {
        __typename
      }
    '''
    response = self.graph_query(url, payload=query)
    try:  
      if response.get('data', {}).get('__typename') == 'Query':
        print('[*] Found GraphQL.')
        return True
      else: 
        raise GraphQLNotFound
    except GraphQLNotFound:
      print('[x] Could not determine existence of GraphQL (GraphQLNotFound)')
    return False

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
    elif self.engine_graphqlphp():
      return 'graphql-php'
    elif self.engine_wpgraphql():
      return 'wpgraphql'
    elif self.engine_graphqlapiforwp():
      return 'graphqlapiforwp'
    elif self.engine_hypergraphql():
      return 'hypergraphql'
    elif self.engine_ruby():
      return 'ruby-graphql'
    return None
  
  def graph_query(self, url, operation='query', payload={}):
    try:
      response = requests.post(url, 
                             headers=self.headers,
                             cookies=self.cookies,
                             allow_redirects=self.follow_redirects,
                             json={operation:payload})
      return response.json()
    except GraphQLError:
      return {}
    except:
      return {}
  def engine_apollo(self):
    preferred_urls = []
    query = '''
      aa
    '''
    response = self.graph_query(self.url, operation='aa', payload=query)
    if response.get('errors'):
      for i in response['errors']:
        if i.get('message') == 'GraphQL operations must contain a non-empty `query` or a `persistedQuery` extension.':
          return True
  
  def engine_graphene(self):
    preferred_urls = []

    query = '''
      { __schema }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        if i.get('message', '') == 'Field "__schema" of type "__Schema!" must have a sub selection.':
          return True

    query = '''aaa'''
    response = self.graph_query(self.url, payload=query)
    
    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Syntax Error GraphQL (1:1)' in err_message:
          return True

    return False
   
  def engine_hasura(self):
    preferred_urls = []
    query = '''
      { __schema }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'missing selection set for "__Schema"' in err_message:
          return True

    query = '''
      { aa }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message')
        if err_message and 'field "aaa" not found in type: \'query_root\'' in err_message:
          return True
  
  def engine_graphqlphp(self):
    preferred_urls = []
    query = '''
      { __schema }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Field "__schema" of type "__Schema!" must have a sub selection.' in err_message:
          return True
    
    query = '''
      { 
        subscription  {
          s
        }
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Schema is not configured for subscriptions.' in err_message:
          return True
        
  def engine_ruby(self):
    preferred_urls = []
    query = '''
      aa@aa {
       __schema {
           directives {
             description
           }
        }
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if err_message == 'Directive @aa is not defined':
          return True
  
    query = '''
      { __schema }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Field must have selections (field \'__schema\' returns __Schema but has no selections.' in err_message:
          return True
    
  def engine_hypergraphql(self):
    preferred_urls = []
    query = '''
      aaa@aaa { 
        __typename 
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Validation error of type UnknownDirective: Unknown directive aaa' in err_message:
          return True
        
        validation_err_type = i.get('validationErrorType', '')
        if validation_err_type == 'UnknownDirective':
          return True
  
  def engine_ariadne(self):
    preferred_urls = []
    query = '''
      { __schema }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Field \'__schema\' of type \'__Schema!\' must have a selection of subfields.' in err_message:
          return True
    
    query = '''
      { 
        subscription {
          s
        }
      }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Could not connect to websocket endpoint' in err_message:
          return True
    
    return False
  
  def engine_graphqlapiforwp(self):
    preferred_urls = []
    query = ''' {
       alias1$1:__schema
     }
    '''
    response = self.graph_query(self.url, payload=query)

    try:
      if response['data']['alias1$1'] == '__schema':
        return True
    except KeyError:
      pass

    query = ''' {
       query aa#aa { __typename }
     }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Unexpected token "END"' in err_message:
          return True
    
    
    return False

  def engine_wpgraphql(self):
    preferred_urls = []
    query = ''' {
       alias1$1:__schema
     }
    '''
    response = self.graph_query(self.url, payload=query)

    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if 'Syntax Error: Expected Name, found $' not in err_message:
          return False
      try:
        debug_msg = response['extensions']['debug'][0]
        if debug_msg['type'] == 'DEBUG_LOGS_INACTIVE' or \
          debug_msg['message'] == 'GraphQL Debug logging is not active. To see debug logs, GRAPHQL_DEBUG must be enabled.':
          return True
      except KeyError:
        pass


