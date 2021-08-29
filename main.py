#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import conf

from graphw00f.helpers import (
  get_time, 
  draw_art, 
  get_engines, 
  user_confirmed
)
from time import sleep
from urllib.parse import urlparse
from optparse import OptionParser

from version import VERSION
from graphw00f.lib import GRAPHW00F


def main():
    parser = OptionParser(usage='%prog -t http://example.com/graphql')
    parser.add_option('-r', '--noredirect', action='store_false', dest='followredirect', default=True, 
                     
                            help='Do not follow redirections given by 3xx responses')
    parser.add_option('-t', '--target', dest='url', help='target url with the path')
    parser.add_option('-o', '--output-file', dest='output_file', 
                            help='Output results to a file (CSV)', default=None)
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False, 
                            help='List all GraphQL technologies graphw00f is able to detect')
    parser.add_option('--version', '-v', dest='version', action='store_true', default=False, 
                            help='Print out the current version and exit.')
    options, args = parser.parse_args()

    if options.list:
      print(draw_art())
      for k, v in graphw00f.helpers.get_engines().items():
        print('{key}: {name} ({language})'.format(
                                            key=k,
                                            name=v['name'],
                                            language=', '.join(v['language']))
                                           )
      sys.exit(0)
  
    if options.version:
      print('version:', VERSION)
      sys.exit(0)

    if not options.url:
      parser.print_help()
      sys.exit(1)
    
    url = options.url
    url_path = urlparse(url).path
    url_scheme = urlparse(url).scheme
    url_netloc = urlparse(url).netloc
    
    print(draw_art())

    if url_scheme not in ('http', 'https'):
      print('URL is missing a scheme (http|https)')
      sys.exit(1)
    
    if not url_netloc:
      print('url {url} does not seem right.'.format(url=url))
      sys.exit(1)

    if not url_path:
      print('[*] No URL path was provided.')
      print('[*[ are you sure you want to fingerprint the server without a path? [y/n]')
      choice = input().lower()
      if not user_confirmed(choice):
        sys.exit(1)

    
    print('[*] Checking if GraphQL is available at {url}...'.format(url=url))
    
    g = GRAPHW00F(follow_redirects=options.followredirect,
                  headers=conf.HEADERS, 
                  cookies=conf.COOKIES)
    detected = None
    
    if g.check(url):
      print('[*] Found GraphQL.')
    else:
      print('[*] Continue anyway? [y/n]'.format(url=url))
      
      choice = input().lower()
      if not user_confirmed(choice):
        print('Quitting.')
        sys.exit(1)
    
    print('[*] Attempting to fingerprint...')
    result = g.execute(url)
    
    if result:
      name = get_engines()[result]['name']
      url = get_engines()[result]['url']
      ref = get_engines()[result]['ref']
      technologies = ', '.join(get_engines()[result]['technology'])
      detected = name
      print('[*] Discovered GraphQL Engine!')
      print('[!] The site {} is using: {}'.format(url, name))
      print('[!] Attack Surface Matrix: {}'.format(ref))
      print('[!] Technologies: {}'.format(technologies))
      print('[!] Homepage: {}'.format(url))
    
    if options.output_file:
      f = open(options.output_file, 'w')
      f.write('url,detected_engine,timestamp\n')
      f.write('{},{},{}\n'.format(url_netloc, detected, get_time()))
      f.close()
    
    print('[*] DONE.')

if __name__ == '__main__':
    main()
    