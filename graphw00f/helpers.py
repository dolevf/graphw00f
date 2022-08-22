
import datetime
import os.path
from urllib.parse import urlparse
from version import VERSION

class bcolors:
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

def read_custom_wordlist(location):
  wordlists = set()
  if os.path.exists(location):
    f = open(location, 'r').read()
    for line in f.splitlines():
      if not line.startswith('/'):
        line = '/' + line

      wordlists.add(line)
  else:
    print('Could not find wordlist file: {}'.format(location))
  return wordlists

def error_contains(response, word_to_match, part='message'):
  if isinstance(response, dict):
    if response.get('errors'):
      for i in response['errors']:
        err_message = i.get(part, '')
        if word_to_match in err_message:
          return True
    return False

def get_time():
  return datetime.datetime.now().strftime('%Y-%m-%d')

def draw_art():
  return '''
                +-------------------+
                |     graphw00f     |
                +-------------------+
                  ***            ***
                **                  **
              **                      **
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
           Dolev Farhi <dolev@lethalbit.com>
  '''.format(version=VERSION)

def possible_graphql_paths():
  return [
    '/',
    '/graphql',
    '/graphiql',
    '/v1/graphql',
    '/v2/graphql',
    '/v3/graphql',
    '/v1/graphiql',
    '/v2/graphiql',
    '/v3/graphiql',
    '/api/graphql',
    '/api/graphiql',
    '/console',
    '/playground',
    '/gql',
    '/query',
    '/index.php?graphql'
  ]

def get_engines():
  return {
    'apollo':{
      'name':'Apollo',
      'url':'https://www.apollographql.com',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/apollo.md',
      'technology':['JavaScript', 'Node.js', 'TypeScript']
    },
    'aws-appsync':{
      'name':'AWS AppSync',
      'url':'https://aws.amazon.com/appsync',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/appsync.md',
      'technology':[],
    },
    'graphene':{
      'name':'Graphene',
      'url':'https://graphene-python.org',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphene.md',
      'technology':['Python']
    },
    'hasura':{
      'name':'Hasura',
      'url':'https://hasura.io',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/hasura.md',
      'technology':['Haskell']
    },
    'graphql-php':{
      'name':'GraphQL PHP',
      'url':'https://webonyx.github.io/graphql-php',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphql-php.md',
      'technology':['PHP']
    },
    'ruby-graphql':{
      'name':'Ruby GraphQL',
      'url':'https://graphql-ruby.org',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphql-ruby.md',
      'technology':['Ruby']
    },
    'hypergraphql':{
      'name':'HyperGraphQL',
      'url':'https://www.hypergraphql.org',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/hypergraphql.md',
      'technology':['Java']
    },
    'ariadne':{
      'name':'Ariadne',
      'url':'https://ariadnegraphql.org',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/ariadne.md',
      'technology':['Python']
    },
    'graphql-api-for-wp':{
      'name':'GraphQL API for Wordpress',
      'url':'https://graphql-api.com',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphql-api-for-wp.md',
      'technology':['PHP'],
    },
    'wpgraphql':{
      'name':'WPGraphQL WordPress Plugin',
      'url':'https://www.wpgraphql.com',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/wp-graphql.md',
      'technology':['PHP']
    },
    'gqlgen':{
      'name':'gqlgen - GraphQL for Go',
      'url':'https://gqlgen.com',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/gqlgen.md',
      'technology':['Go']
    },
    'graphql-go':{
      'name':'graphql-go -GraphQL for Go',
      'url':'https://github.com/graphql-go/graphql',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphql-go.md',
      'technology':['Go']
    },
    'graphql-java':{
      'name':'graphql-java - GraphQL for Java',
      'url':'https://www.graphql-java.com',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphql-java.md',
      'technology':['Java']
    },
    'juniper':{
      'name':'Juniper - GraphQL for Rust',
      'url':'https://graphql-rust.github.io',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/juniper.md',
      'technology':['Rust']
    },
    'sangria':{
      'name':'Sangria - GraphQL for Scala',
      'url':'https://sangria-graphql.github.io',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/sangria.md',
      'technology':['Scala']
    },
    'flutter':{
      'name':'Flutter - GraphQL for Dart',
      'url':'https://github.com/zino-app/graphql-flutter',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/gql-dart.md',
      'technology':['Dart']
    },
    'dianajl':{
      'name':'Diana.jl - GraphQL for Julia',
      'url':'https://github.com/neomatrixcode/Diana.jl',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/diana.md',
      'technology':['Julia']
    },
    'strawberry':{
      'name':'Strawberry - GraphQL for Python',
      'url':'https://github.com/strawberry-graphql/strawberry',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/strawberry.md',
      'technology':['Python']
    },
    'tartiflette':{
      'name':'tartiflette - GraphQL for Python',
      'url':'https://github.com/tartiflette/tartiflette',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/tartiflette.md',
      'technology':['Python']
    },
    'dgraph':{
      'name':'Dgraph',
      'url':'https://dgraph.io/',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/dgraph.md',
      'technology':['JavaScript']
    },
    'directus':{
      'name':'Directus',
      'url':'https://directus.io/',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/directus.md',
      'technology':['TypeScript']
    },
    'graphql_yoga':{
      'name':'GraphQL Yoga',
      'url':'https://github.com/dotansimha/graphql-yoga',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphql-yoga.md',
      'technology':['TypeScript']
    },
    'lighthouse':{
      'name':'Lighthouse',
      'url':'https://github.com/nuwave/lighthouse',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/lighthouse.md',
      'technology':['PHP']
    },
    'agoo':{
      'name':'Agoo',
      'url':'https://github.com/ohler55/agoo',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/agoo.md',
      'technology':['Ruby']
    },
    'mercurius':{
      'name':'mercurius',
      'url':'https://github.com/mercurius-js/mercurius',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/agoo.md',
      'technology':['JavaScript', 'Node.js', 'TypeScript']
    },
    'morpheus-graphql':{
      'name':'morpheus-graphql',
      'url':'https://github.com/morpheusgraphql/morpheus-graphql',
      'ref':'https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/morpheus-graphql',
      'technology':['Haskell']
    }
  }

def user_confirmed(choice):
  if choice in ('yes', 'y'):
   return True
  return False
