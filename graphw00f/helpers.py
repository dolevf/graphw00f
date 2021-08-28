
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
      'language':['JavaScript']
    },
    'graphene':{
      'name':'Graphene',
      'url':'https://graphene-python.org',
      'language':['Python']
    },
    'hasura':{
      'name':'Hasura',
      'url':'https://hasura.io',
      'language':['Haskell']
    },
    'graphql-php':{
      'name':'GraphQL PHP',
      'url':'https://webonyx.github.io/graphql-php',
      'language':['PHP']
    },
    'ruby-graphql':{
      'name':'Ruby GraphQL',
      'url':'https://graphql-ruby.org',
      'language':['Ruby']
    },
    'hypergraphql':{
      'name':'HyperGraphQL',
      'url':'https://www.hypergraphql.org',
      'language':['Java']
    },
    'ariadne':{
      'name':'Ariadne',
      'url':'https://ariadnegraphql.org',
      'language':['Python']
    },
    'graphqlapiforwp':{
      'name':'GraphQL API for Wordpress',
      'url':'https://graphql-api.com',
      'language':['PHP'],
    },
    'wpgraphql':{
      'name':'WPGraphQL WordPress Plugin',
      'url':'https://www.wpgraphql.com',
      'language':['PHP']
    },
    'gqlgen':{
      'name':'gqlgen - GraphQL for Go',
      'url':'https://gqlgen.com',
      'language':['Go']
    }
  }

def user_confirmed(choice):
  if choice in ('yes', 'y'):
   return True
  return False
