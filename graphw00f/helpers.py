
import datetime
from urllib.parse import urlparse
from version import VERSION

def error_contains(response, word_to_match):
  if isinstance(response, dict):
    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get('message', '')
        if word_to_match in err_message:
          return True
    return False

def get_time():
  return datetime.datetime.now().strftime('%Y-%m-%d')

def draw_art():
  return '''
+-------------------+           +--------------------+
|      GRAPHQL      |           |     FINGERPRINT    |
+-------------------+           +--------------------+
                  **              **                  
                    ***        ***                    
                       **    **                       
                +-------------------+                 
                |     graphw00f     |                 
                +-------------------+                 
                  ***            ***                  
                **                  ***               
              **                       **             
    +--------------+              +--------------+       
    |    Node X    |              |    Node Y    |       
    +--------------+              +--------------+     
                  ***            ***                  
                     **        **                     
                       **    **                       
                    +------------+                      
                    |   Node Z   |                      
                    +------------+    

                graphw00f - v{version}
          The fingerprinting tool for GraphQL
  '''.format(version=VERSION)

def get_engines():
  return {
    'apollo':{
      'name':'Apollo',
      'url':'https://www.apollographql.com',
      'technology':['JavaScript', 'Node.js', 'TypeScript']
    },
    'graphene':{
      'name':'Graphene',
      'url':'https://graphene-python.org',
      'technology':['Python']
    },
    'hasura':{
      'name':'Hasura',
      'url':'https://hasura.io',
      'technology':['Haskell']
    },
    'graphql-php':{
      'name':'GraphQL PHP',
      'url':'https://webonyx.github.io/graphql-php',
      'technology':['PHP']
    },
    'ruby-graphql':{
      'name':'Ruby GraphQL',
      'url':'https://graphql-ruby.org',
      'technology':['Ruby']
    },
    'hypergraphql':{
      'name':'HyperGraphQL',
      'url':'https://www.hypergraphql.org',
      'technology':['Java']
    },
    'ariadne':{
      'name':'Ariadne',
      'url':'https://ariadnegraphql.org',
      'technology':['Python']
    },
    'graphql-api-for-wp':{
      'name':'GraphQL API for Wordpress',
      'url':'https://graphql-api.com',
      'technology':['PHP'],
    },
    'wpgraphql':{
      'name':'WPGraphQL WordPress Plugin',
      'url':'https://www.wpgraphql.com',
      'technology':['PHP']
    },
    'gqlgen':{
      'name':'gqlgen - GraphQL for Go',
      'url':'https://gqlgen.com',
      'technology':['Go']
    },
    'graphql-go':{
      'name':'graphql-go -GraphQL for Go',
      'url':'https://github.com/graphql-go/graphql',
      'technology':['Go']
    }
  }

def user_confirmed(choice):
  if choice in ('yes', 'y'):
   return True
  return False
