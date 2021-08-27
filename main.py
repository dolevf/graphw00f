#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import conf
import graphw00f.helpers

from urllib.parse import urlparse
from optparse import OptionParser

from graphw00f.lib import GRAPHW00F


def main():
    parser = OptionParser()
    parser.add_option('-r', '--noredirect', action='store_false', dest='followredirect', default=True, 
                            help='Do not follow redirections given by 3xx responses')
    parser.add_option('-i', '--input-file', dest='input', 
                            help='Read targets from a file. Expects a single URL per line.', default=None)
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False, 
                            help='List all GraphQL technologies graphw00f is able to detect')
    parser.add_option('--version', '-V', dest='version', action='store_true', default=False, 
                            help='Print out the current version and exit.')
    options, args = parser.parse_args()

    if options.list:
      for k, v in graphw00f.helpers.get_engines().items():
        print('{key}: {name} ({language})'.format(
                                            key=k,
                                            name=v['name'],
                                            language=', '.join(v['language']))
                                           )
      sys.exit(0)
    
    if not args:
      print('Error: you must pass at least 1 url.')
      print(f'{sys.argv[0]} https://site.com/graphql')
      sys.exit(1)
    

    url = args[0]
    url_path = urlparse(url).path
    url_scheme = urlparse(url).scheme
    url_netloc = urlparse(url).netloc

    if url_scheme not in ('http', 'https'):
      print('URL is missing a scheme (http|https)')
      sys.exit(1)
    
    if not url_netloc:
      print('url {url} does not seem right.'.format(url=url))
      sys.exit(1)

    if not url_path:
      print('No URL Path was provided, are you sure you want to scan for graphql without a path?...')
      
    g = GRAPHW00F(input_file=options.input,
                  follow_redirects=options.followredirect,
                  headers=conf.HEADERS, 
                  cookies=conf.COOKIES)
    
    print('[*] Checking if GraphQL is available at {url}...'.format(url=url))
    if not g.check(url):
      print('[x] {url} did not seem to provide a standard GraphQL response, indicating it may not exist.')
      print('[x] graphw00f may fail, continue? [y/n]')
      choice = raw_input().lower()
      if graphw00f.helpers.user_confirmed(choice):
        g.execute(url)
      else:
        print('Quitting.')
        sys.exit(1)
    else:
      print('[*] Running...')
      result = g.execute(url)

      if result:
        name = graphw00f.helpers.get_engines()[result]['name']
        url = graphw00f.helpers.get_engines()[result]['url']
        language = ', '.join(graphw00f.helpers.get_engines()[result]['language'])
        print('[*] Discovered GraphQL Engine!')
        print('\t[!] The site {} is behind {}'.format(url, name))
        print('\t[!] Language: {}'.format(language))
        print('\t[!] Homepage: {}'.format(url))
  

if __name__ == '__main__':
    main()
    