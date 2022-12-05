#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import conf

from graphw00f.helpers import (
  get_time,
  draw_art,
  get_engines,
  user_confirmed,
  read_custom_wordlist,
  possible_graphql_paths,
  bcolors
)

from time import sleep
from urllib.parse import urlparse
from optparse import OptionParser

from version import VERSION
from graphw00f.lib import (
  GRAPHW00F,
  GraphQLDetectionFailed
)


def main():
    parser = OptionParser(usage='%prog -d -f -t http://example.com')
    parser.add_option('-r', '--noredirect', action='store_false', dest='followredirect', default=True,

                            help='Do not follow redirections given by 3xx responses')
    parser.add_option('-t', '--target', dest='url', help='target url with the path')
    parser.add_option('-f', '--fingerprint', dest='fingerprint', default=False, action='store_true', help='fingerprint mode')
    parser.add_option('-d', '--detect', dest='detect', default=False, action='store_true', help='detect mode')
    parser.add_option('-p', '--proxy', dest='proxy', default=None, help='HTTP(S) proxy URL in the form http://user:pass@host:port')
    parser.add_option('-b', '--burp', dest='burp', default=False, action='store_true',
                            help='Sets the proxy to http://127.0.0.1:8080. Overridden by --proxy')
    parser.add_option('-T', '--timeout', dest='timeout', default=10, help='Request timeout in seconds')
    parser.add_option('-o', '--output-file', dest='output_file',
                            help='Output results to a file (CSV)', default=None)
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False,
                            help='List all GraphQL technologies graphw00f is able to detect')
    parser.add_option('-u', '--user-agent', dest='useragent', default=None, help='Custom user-agent to use (overrides the one from headers configuration)')
    parser.add_option('-w', '--wordlist', dest='wordlist', default=False, help='Path to a list of custom GraphQL endpoints')
    parser.add_option('--version', '-v', dest='version', action='store_true', default=False,
                            help='Print out the current version and exit.')
    options, args = parser.parse_args()

    if options.list:
      print(draw_art())
      count = 0
      for k, v in get_engines().items():
        count += 1
        print('{index}. {name} ({technology})'.format(
                                            index=count,
                                            name=v['name'],
                                            technology=', '.join(v['technology']))
                                           )
      sys.exit(0)

    if options.version:
      print('version:', VERSION)
      sys.exit(0)

    if not options.url:
      parser.print_help()
      sys.exit(1)

    if not options.detect and not options.fingerprint:
      parser.print_help()
      sys.exit(1)

    proxies = None

    if options.burp:
      proxies = {
          'http': 'http://127.0.0.1:8080',
          'https': 'https://127.0.0.1:8080'
      }

    if options.proxy:
      proxies = {
          'http': options.proxy,
          'https': options.proxy
      }

    if not isinstance(options.timeout, int):
      options.timeout = 10

    g = GRAPHW00F(follow_redirects=options.followredirect,
                  headers=conf.HEADERS if not options.useragent else {**conf.HEADERS, **{'User-Agent': options.useragent}},
                  cookies=conf.COOKIES,
                  timeout=options.timeout,
                  proxies=proxies)
    url = options.url

    url_scheme = urlparse(url).scheme
    url_netloc = urlparse(url).netloc
    wordlist = possible_graphql_paths()
    detected = False
    print(draw_art())

    if url_scheme not in ('http', 'https'):
      print('URL is missing a scheme (http|https)')
      sys.exit(1)

    if not url_netloc:
      print('url {url} does not seem right.'.format(url=url))
      sys.exit(1)

    if options.burp and options.proxy:
      print(bcolors.WARNING + '[!] Both --proxy and --burp options supplied, overriding --burp.' + bcolors.ENDC)

    if options.detect:
      if options.wordlist:
        wordlist = read_custom_wordlist(options.wordlist)

      for endpoint in wordlist:
        target = url + endpoint
        print('[*] Checking {}'.format(target))
        try:
          g.check(target)
          print('[!] Found GraphQL at {}'.format(target))
          url = target
          detected = True

          if not options.fingerprint:
            sys.exit(0)

          break
        except GraphQLDetectionFailed:
          continue
      if not detected:
        print('[x] Could not find GraphQL anywhere.')
        sys.exit(1)
    else:
      print('[*] Checking if GraphQL is available at {url}...'.format(url=url))  
      fingerprint = None
      try:
        if g.check(url):
          print('[!] Found GraphQL.')
      except GraphQLDetectionFailed:
          print(bcolors.FAIL + '[x] Could not determine the existence of GraphQL (Error: GraphQLDetectionFailed)' + bcolors.ENDC)
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
      fingerprint = name
      print(bcolors.OKGREEN + '[*] Discovered GraphQL Engine: ({})'.format(name))
      print('[!] Attack Surface Matrix: {}'.format(ref))
      print('[!] Technologies: {}'.format(technologies))
      print('[!] Homepage: {}'.format(url))
    else:
      print('[x] Nothing was found :-(')

    if options.output_file:
      f = open(options.output_file, 'w')
      f.write('url,detected_engine,timestamp\n')
      f.write('{},{},{}\n'.format(url_netloc, fingerprint, get_time()))
      f.close()
    
    print(bcolors.ENDC + '[*] Completed.')

if __name__ == '__main__':
    main()
    