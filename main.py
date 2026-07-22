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
    parser.add_option('-T', '--timeout', dest='timeout', default=10, help='Request timeout in seconds')
    parser.add_option('-o', '--output-file', dest='output_file',
                            help='Output results to a file (CSV)', default=None)
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False,
                            help='List all GraphQL technologies graphw00f is able to detect')
    parser.add_option('-u', '--user-agent', dest='useragent', default=None, help='Custom user-agent to use (overrides the one from headers configuration)')
    parser.add_option('-H', '--header', dest='header', action='append', default=[], help='Custom headers to send (e.g. "Authorization: Bearer ey...").')
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
    if options.proxy:
      proxies = {
          'http': options.proxy,
          'https': options.proxy
      }

    if not isinstance(options.timeout, int):
      options.timeout = 10

    headers = {}
    headers["User-Agent"] = conf.HEADERS["User-Agent"]

    # Read configuration headers
    for header in conf.HEADERS:
        headers[header] = conf.HEADERS[header]

    for header in options.header:
      key, value = header.split(": ")
      headers[key] = value    

    if options.useragent:
      headers["User-Agent"] = options.useragent

    print(headers)
    g = GRAPHW00F(follow_redirects=options.followredirect,
                  headers=headers,
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
    fingerprint = None
    result = g.execute(url)
    detail = g.last_result or {}
    confidence = detail.get('confidence')
    family = detail.get('family')

    if result:
      engines = get_engines()
      meta = engines.get(result, {'name': result, 'url': '', 'ref': '', 'technology': []})
      name = meta['name']
      home = meta.get('url', '')
      ref = meta.get('ref', '')
      technologies = ', '.join(meta.get('technology', []))
      fingerprint = name

      conf_color = {'high': bcolors.OKGREEN, 'medium': bcolors.OKCYAN, 'low': bcolors.WARNING}.get(confidence, bcolors.OKGREEN)
      print(conf_color + '[*] Discovered GraphQL Engine: ({})'.format(name))
      if confidence:
        print('[!] Confidence: {} (family: {}, score: {})'.format(confidence.upper(), family, detail.get('score')))
      if confidence == 'low':
        print(bcolors.WARNING + '[i] Only library-family evidence was observed — no server-unique signal. '
              'Reported as the underlying engine, not a specific server.' + bcolors.ENDC)
      # Evidence: which probe strings actually fired
      for sig in detail.get('signals', []):
        _eng, _fam, _w, _pid, _kind, _arg = sig
        print('    [+] signal: probe={} kind={} match={!r} (weight {})'.format(_pid, _kind, _arg, _w))
      if detail.get('federation'):
        print(bcolors.OKCYAN + '[!] Apollo Federation / supergraph detected (query { _service { sdl } } returned SDL).' + bcolors.ENDC)
      if detail.get('ambiguous'):
        runners = ', '.join('{} ({})'.format(e, s) for e, s in detail.get('runners', []))
        print(bcolors.WARNING + '[i] Ambiguous — other strong candidates: {}'.format(runners) + bcolors.ENDC)
      print('[!] Attack Surface Matrix: {}'.format(ref))
      print('[!] Technologies: {}'.format(technologies))
      print('[!] Homepage: {}'.format(home))
    else:
      print('[x] Nothing was found :-(')

    if options.output_file:
      f = open(options.output_file, 'w')
      f.write('url,detected_engine,family,confidence,timestamp\n')
      f.write('{},{},{},{},{}\n'.format(url_netloc, fingerprint, family or '', confidence or '', get_time()))
      f.close()
    
    print(bcolors.ENDC + '[*] Completed.')

if __name__ == '__main__':
    main()
    
