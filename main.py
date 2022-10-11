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
)
from graphw00f.logger import logger, setup_logger

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
    parser.add_option('-T', '--timeout', dest='timeout', default=10, help='Request timeout in seconds')
    parser.add_option('-o', '--output-file', dest='output_file',
                            help='Output results to a file (CSV)', default=None)
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False,
                            help='List all GraphQL technologies graphw00f is able to detect')
    parser.add_option('-u', '--user-agent', dest='useragent', default=None, help='Custom user-agent to use (overrides the one from headers configuration)')
    parser.add_option('-w', '--wordlist', dest='wordlist', default=False, help='Path to a list of custom GraphQL endpoints')
    parser.add_option('--version', '-v', dest='version', action='store_true', default=False,
                            help='Print out the current version and exit.')
    options, _ = parser.parse_args()

    if options.list:
      print(draw_art())
      count = 0
      for v in get_engines().values():
        count += 1
        print(f'{count}. {v["name"]} ({"".join(v["technology"])}')

      sys.exit(0)

    if options.version:
      logger.info(f'version: {VERSION}')
      sys.exit(0)

    if not options.url:
      parser.print_help()
      sys.exit(1)

    if not options.detect and not options.fingerprint:
      parser.print_help()
      sys.exit(1)

    if not isinstance(options.timeout, int):
      options.timeout = 10

    g = GRAPHW00F(follow_redirects=options.followredirect,
                  headers=conf.HEADERS if not options.useragent else {**conf.HEADERS, **{'User-Agent': options.useragent}},
                  cookies=conf.COOKIES,
                  timeout=options.timeout)
    url = options.url

    url_scheme = urlparse(url).scheme
    url_netloc = urlparse(url).netloc
    wordlist = possible_graphql_paths()
    detected = False

    if url_scheme not in ('http', 'https'):
      logger.critical('URL is missing a scheme (http|https)')
      sys.exit(1)

    if not url_netloc:
      logger.critical(f'url {url} does not seem right.')
      sys.exit(1)

    if options.detect:
      if options.wordlist:
        wordlist = read_custom_wordlist(options.wordlist)

      for endpoint in wordlist:
        target = url + endpoint
        logger.debug(f'[*] Checking {target}')
        try:
          g.check(target)
          logger.info(f'[!] Found GraphQL at {target}')
          url = target
          detected = True

          if not options.fingerprint:
            sys.exit(0)

          break
        except GraphQLDetectionFailed:
          continue
      if not detected:
        logger.info('[x] Could not find GraphQL anywhere.')
        sys.exit(1)
    else:
      logger.debug(f'[*] Checking if GraphQL is available at {url}...')  
      fingerprint = None
      try:
        if g.check(url):
          logger.info('[!] Found GraphQL.')
      except GraphQLDetectionFailed:
          logger.error('[x] Could not determine the existence of GraphQL (Error: GraphQLDetectionFailed)')
          logger.info('[*] Continue anyway? [y/n]')
          choice = input().lower()
          if not user_confirmed(choice):
            logger.info('Quitting.')
            sys.exit(1)

    logger.debug('[*] Attempting to fingerprint...')
    result = g.execute(url)

    if result:
      name = get_engines()[result]['name']
      url = get_engines()[result]['url']
      ref = get_engines()[result]['ref']
      technologies = ', '.join(get_engines()[result]['technology'])
      fingerprint = name
      logger.info(f'[*] Discovered GraphQL Engine: ({name})')
      logger.info(f'[!] Attack Surface Matrix: {ref}')
      logger.info(f'[!] Technologies: {technologies}')
      logger.info(f'[!] Homepage: {url}')
    else:
      logger.info('[x] Nothing was found :-(')

    if options.output_file:
      f = open(options.output_file, 'w')
      f.write('url,detected_engine,timestamp\n')
      f.write(f'{url_netloc},{fingerprint},{get_time()}\n')
      f.close()
    
    logger.debug('[*] Completed.')

if __name__ == '__main__':
    setup_logger()
    main()
    