import requests

def list_engines():
   return {
      'apollo':{
        'name':'Apollo',
        'language':['JavaScript']
      },
      'graphene':{
        'name':'Graphene',
        'language':['Python']
      },
      'hasura':{
        'name':'Hasura',
        'language':['Haskell']
      },
      'graphqlphp':{
        'name':'graphql-php',
        'language':['PHP']
      },
      'ruby-graphql':{
        'name':'Ruby GraphQL',
        'language':['Ruby']
      },
      'hypergraphql':{
        'name':'HyperGraphQL',
        'language':['Java']
      },
      'ariadne':{
        'name':'Ariadne',
        'language':['Python']
      },
      'graphqlapiforwp':{
        'name':'GraphQL API for Wordpress',
        'language':['PHP'],
      },
      'wpgraphql':{
        'name':'WPGraphQL Plugin',
        'language':['PHP']
      }
    }


class GRAPHW00F:
  def __init__(self, url, 
                     headers,
                     cookies,
                     selected_engine=None, 
                     input_file=None, 
                     follow_redirects=False):
    self.url = url
    self.cookies = cookies
    self.headers = headers or {'User-Agent':'graphw00f'}
    self.selected_engine = selected_engine
    self.input_file = input_file
    self.follow_redirects = follow_redirects
    self.defaut_urls = ['/graphql']
    

  def detect(self):
    pass
    # self.engines[self.selected_engine]['func']()
    
  def engine_apollo(self):
    preferred_urls = []
  
  def engine_graphene(self):
    preferred_urls = []
  
  def engine_hasura(self):
    preferred_urls = []
  
  def engine_graphene(self):
    preferred_urls = []
  
  def engine_graphqlphp(self):
    preferred_urls = []
   
  def engine_ruby(self):
    preferred_urls = []
  
  def engine_hypergraphql(self):
    preferred_urls = []
  
  def engine_ariadne(self):
    preferred_urls = []
  
  def engine_graphqlapiforwp(self):
    preferred_urls = []
    
  def engine_wpgraphql(self):
    preferred_urls = []
    