
import datetime
from urllib.parse import urlparse
from version import VERSION

class bcolors:
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

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
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/apollo.md',
      'technology':['JavaScript', 'Node.js', 'TypeScript']
    },
    'graphene':{
      'name':'Graphene',
      'url':'https://graphene-python.org',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/graphene.md',
      'technology':['Python']
    },
    'hasura':{
      'name':'Hasura',
      'url':'https://hasura.io',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/hasura.md',
      'technology':['Haskell']
    },
    'graphql-php':{
      'name':'GraphQL PHP',
      'url':'https://webonyx.github.io/graphql-php',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/graphql-php.md',
      'technology':['PHP']
    },
    'ruby-graphql':{
      'name':'Ruby GraphQL',
      'url':'https://graphql-ruby.org',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/ruby-graphql.md',
      'technology':['Ruby']
    },
    'hypergraphql':{
      'name':'HyperGraphQL',
      'url':'https://www.hypergraphql.org',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/hypergraphql.md',
      'technology':['Java']
    },
    'ariadne':{
      'name':'Ariadne',
      'url':'https://ariadnegraphql.org',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/ariadne.md',
      'technology':['Python']
    },
    'graphql-api-for-wp':{
      'name':'GraphQL API for Wordpress',
      'url':'https://graphql-api.com',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/graphqlapiforwp.md',
      'technology':['PHP'],
    },
    'wpgraphql':{
      'name':'WPGraphQL WordPress Plugin',
      'url':'https://www.wpgraphql.com',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/wpgraphql.md',
      'technology':['PHP']
    },
    'gqlgen':{
      'name':'gqlgen - GraphQL for Go',
      'url':'https://gqlgen.com',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/gqlgen.md',
      'technology':['Go']
    },
    'graphql-go':{
      'name':'graphql-go -GraphQL for Go',
      'url':'https://github.com/graphql-go/graphql',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/graphql-go.md',
      'technology':['Go']
    },
    'graphql-java':{
      'name':'graphql-java - GraphQL for Java',
      'url':'https://www.graphql-java.com',
      'ref':'https://github.com/dolevf/graphw00f/blob/main/docs/graphql-java.md',
      'technology':['Java']
    }
  }

def user_confirmed(choice):
  if choice in ('yes', 'y'):
   return True
  return False
