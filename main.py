#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import conf
import graphw00f.helpers

from time import sleep
from urllib.parse import urlparse
from optparse import OptionParser

from graphw00f.lib import GRAPHW00F


def main():
    parser = OptionParser()
    parser.add_option('-r', '--noredirect', action='store_false', dest='followredirect', default=True, 
                            help='Do not follow redirections given by 3xx responses')
    parser.add_option('-o', '--output-file', dest='output_file', 
                            help='Output results to a file (CSV)', default=None)
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False, 
                            help='List all GraphQL technologies graphw00f is able to detect')
    parser.add_option('--version', '-V', dest='version', action='store_true', default=False, 
                            help='Print out the current version and exit.')
    options, args = parser.parse_args()

    if options.list:
      print(graphw00f.helpers.draw_art())
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
    detected = None
    
    g = GRAPHW00F(follow_redirects=options.followredirect,
                  headers=conf.HEADERS, 
                  cookies=conf.COOKIES)

    print(graphw00f.helpers.draw_art())

    if url_scheme not in ('http', 'https'):
      print('URL is missing a scheme (http|https)')
      sys.exit(1)
    
    if not url_netloc:
      print('url {url} does not seem right.'.format(url=url))
      sys.exit(1)

    if not url_path:
      print('[*] No URL Path was provided, are you sure you want to scan for graphql without a path?...')
      print('[*[ Continue anyway? [y/n]')
      choice = input().lower()
      if not graphw00f.helpers.user_confirmed(choice):
        sys.exit(1)

    print('[*] Checking if GraphQL is available at {url}...'.format(url=url))

    if not g.check(url):
      print('[*] Continue anyway? [y/n]'.format(url=url))
      choice = input().lower()
      if graphw00f.helpers.user_confirmed(choice):
        g.execute(url)
      else:
        print('Quitting.')
        sys.exit(1)
    else:
      print('[*] Attempting to fingerprint...')
      result = g.execute(url)
      if result:
        name = graphw00f.helpers.get_engines()[result]['name']
        url = graphw00f.helpers.get_engines()[result]['url']
        language = ', '.join(graphw00f.helpers.get_engines()[result]['language'])
        detected = name
        print('[*] Discovered GraphQL Engine!')
        print('[!] The site {} is using: {}'.format(url, name))
        print('[!] Language: {}'.format(language))
        print('[!] Homepage: {}'.format(url))
        

    if options.output_file:
      f = open(options.output_file, 'w')
      f.write('url,detected_engine,timestamp\n')
      f.write('{},{},{}\n'.format(url_netloc, detected, graphw00f.helpers.get_time()))
      f.close()

if __name__ == '__main__':
    main()
    