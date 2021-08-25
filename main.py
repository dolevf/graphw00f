#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from optparse import OptionParser
from graphw00f.engines import GRAPHW00F, list_engines
from conf import COOKIES, HEADERS

def main():
    parser = OptionParser()
    parser.add_option('-r', '--noredirect', action='store_false', dest='followredirect', default=True, 
                            help='Do not follow redirections given by 3xx responses')
    parser.add_option('-t', '--test', dest='test', 
                            help='Test for one specific GraphQL technology')
    parser.add_option('-i', '--input-file', dest='input', 
                            help='Read targets from a file. Expects a single URL per line.', default=None)
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False, 
                            help='List all GraphQL technologies graphw00f is able to detect')
    parser.add_option('--version', '-V', dest='version', action='store_true', default=False, 
                            help='Print out the current version and exit.')
    options, url = parser.parse_args()

    if options.list:
      for k, v in list_engines().items():
        print('{key}: {name} ({language})'.format(
                                            key=k,
                                            name=v['name'],
                                            language=', '.join(v['language']))
                                           )
      sys.exit(0)
    
    if not options.input and not url:
      print('Error: you must pass at least 1 url.')
      print(f'{sys.argv[0]} https://site.com/graphql')
      sys.exit(1)
    
    selected_engine = options.test
    input_file = options.input
    headers = options.headers
    cookies = options.cookies
    follow_redirects = options.followredirect

    if selected_engine:
      if selected_engine not in list_engines().keys():
        print('\nError: {engine} is not supported'.format(engine=selected_engine))
    
    g = GRAPHW00F(url, selected_engine=selected_engine,
                       input_file=input_file,
                       headers=HEADERS, 
                       cookies=COOKIES, 
                       follow_redirects=follow_redirects)
    
    result = g.detect()


if __name__ == '__main__':
    main()
    