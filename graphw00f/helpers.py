
from urllib.parse import urlparse

VERSION = '1.0.0'

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
    +--------------+                     **           
    |    Node A    |                   **             
    +--------------+                ***               
                  ***            ***                  
                     **        **                     
                       **    **                       
                    +------------+                      
                    |   Node X   |                      
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
    }
  }

def user_confirmed(choice):
  if choice in ('yes', 'y'):
   return True
  return False
