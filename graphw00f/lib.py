import requests

from collections import defaultdict

from graphw00f.helpers import error_contains
from graphw00f.matcher import (
  PROBES,
  SIGNALS,
  FAMILY_FALLBACK,
  UNIQUE,
  STRONG,
  FAMILY,
)

requests.packages.urllib3.disable_warnings()


class GraphQLDetectionFailed(Exception):
  pass


class GraphQLError(Exception):
  pass


class GRAPHW00F:
  def __init__(self, headers,
                     cookies,
                     timeout,
                     proxies,
                     follow_redirects=False):
    self.url = 'http://example.com'
    self.cookies = cookies
    self.headers = headers
    self.follow_redirects = follow_redirects
    self.timeout = timeout
    self.proxies = proxies
    # populated by the last detect_engine() run, for verbose output
    self.last_result = None

  # ---------------------------------------------------------------- detection
  def check(self, url):
    query = '''
      query {
        __typename
      }
    '''
    response, _ = self.graph_query_full(url, payload=query)
    if response.get('data'):
      if response.get('data', {}).get('__typename', '') in ('Query', 'QueryRoot', 'query_root', 'RootQuery', 'RootQueryType'):
        return True
    elif response.get('errors') and (any('locations' in i for i in response['errors']) or any('extensions' in i for i in response['errors'])):
      return True
    elif response.get('data'):
      return True
    else:
      raise GraphQLDetectionFailed

  def execute(self, url):
    '''Backward-compatible entrypoint: returns a single engine id (or None).'''
    result = self.detect_engine(url)
    self.last_result = result
    return result['engine'] if result else None

  # ------------------------------------------------------------- HTTP helpers
  def graph_query_full(self, url, operation='query', payload={}):
    '''Send a probe. Returns (json_dict, headers_dict).

    GraphQL may accept POST or GET (or both). We prefer whichever returns a
    JSON object, and return the matching response's headers so signal
    evaluation can consult them.
    '''
    try:
      response_post = requests.post(url,
                             headers=self.headers,
                             cookies=self.cookies,
                             verify=False,
                             allow_redirects=self.follow_redirects,
                             timeout=self.timeout,
                             proxies=self.proxies,
                             json={operation: payload})
      try:
        pj = response_post.json()
      except Exception:
        pj = None
      if isinstance(pj, dict):
        return pj, dict(response_post.headers)

      response_get = requests.get(url,
                             headers=self.headers,
                             cookies=self.cookies,
                             verify=False,
                             allow_redirects=self.follow_redirects,
                             timeout=self.timeout,
                             proxies=self.proxies,
                             params={operation: payload})
      try:
        gj = response_get.json()
      except Exception:
        gj = None
      if isinstance(gj, dict):
        return gj, dict(response_get.headers)

      return {}, dict(response_post.headers)
    except Exception:
      return {}, {}

  def graph_query(self, url, operation='query', payload={}):
    '''Legacy shim: returns just the JSON body.'''
    body, _ = self.graph_query_full(url, operation=operation, payload=payload)
    return body

  # --------------------------------------------------------------- the engine
  def _raw_json_query(self, url, body):
    '''POST an arbitrary JSON body (for wrapper-layer probes). Returns (json, headers).'''
    try:
      resp = requests.post(url,
                           headers=self.headers,
                           cookies=self.cookies,
                           verify=False,
                           allow_redirects=self.follow_redirects,
                           timeout=self.timeout,
                           proxies=self.proxies,
                           json=body)
      try:
        j = resp.json()
      except Exception:
        j = None
      return (j if isinstance(j, dict) else {}), dict(resp.headers)
    except Exception:
      return {}, {}

  def _html_get(self, url):
    '''Plain GET of the endpoint to capture an IDE landing page (GraphiQL/Sandbox/Playground).'''
    try:
      hdrs = dict(self.headers)
      hdrs['Accept'] = 'text/html,application/xhtml+xml'
      resp = requests.get(url,
                          headers=hdrs,
                          cookies=self.cookies,
                          verify=False,
                          allow_redirects=self.follow_redirects,
                          timeout=self.timeout,
                          proxies=self.proxies)
      return {'__html__': resp.text[:65536]}, dict(resp.headers)
    except Exception:
      return {'__html__': ''}, {}

  def _send_probes(self, url):
    '''Send every probe referenced by the signal table exactly once.'''
    responses = {}
    headers = {}
    used = sorted(set(sig[3] for sig in SIGNALS))
    for pid in used:
      probe = PROBES[pid]
      if isinstance(probe, dict) and '__rawjson__' in probe:
        body, hdrs = self._raw_json_query(url, probe['__rawjson__'])
      elif isinstance(probe, dict) and probe.get('__get_html__'):
        body, hdrs = self._html_get(url)
      else:
        body, hdrs = self.graph_query_full(url, payload=probe)
      responses[pid] = body if isinstance(body, dict) else {}
      headers[pid] = hdrs or {}
    return responses, headers

  @staticmethod
  def _walk(obj, path):
    cur = obj
    for p in path:
      if isinstance(p, int):
        if isinstance(cur, list) and len(cur) > p:
          cur = cur[p]
        else:
          return None
      else:
        if isinstance(cur, dict) and p in cur:
          cur = cur[p]
        else:
          return None
    return cur

  def _match(self, sig, responses, headers):
    engine, family, weight, pid, kind, arg = sig
    resp = responses.get(pid, {}) or {}
    hdrs = headers.get(pid, {}) or {}
    data = resp.get('data') if isinstance(resp, dict) else None

    if kind == 'msg':
      return error_contains(resp, arg)
    if kind == 'nodata_msg':
      return error_contains(resp, arg) and 'data' not in resp
    if kind == 'data_msg':
      return error_contains(resp, arg) and 'data' in resp
    if kind == 'part':
      field, sub = arg
      return error_contains(resp, sub, part=field)
    if kind == 'typename':
      return isinstance(data, dict) and data.get('__typename') == arg
    if kind == 'alias':
      alias, val = arg
      return isinstance(data, dict) and data.get(alias) == val
    if kind == 'field':
      field, val = arg
      return isinstance(data, dict) and data.get(field) == val
    if kind == 'ext_key':
      ext = resp.get('extensions')
      return isinstance(ext, dict) and arg in ext
    if kind == 'ext_code':
      for err in (resp.get('errors') or []):
        if isinstance(err, dict):
          ext = err.get('extensions') or {}
          if isinstance(ext, dict) and ext.get('code') == arg:
            return True
      return False
    if kind == 'ext_field':
      path, val = arg
      base = resp.get('extensions')
      return self._walk(base, path) == val
    if kind == 'ext_present':
      # arg = path tuple into top-level response.extensions; True if it resolves to non-None
      base = resp.get('extensions')
      return self._walk(base, arg) is not None
    if kind == 'err_ext_present':
      # arg = path tuple into any error's .extensions; True if present on any error
      for err in (resp.get('errors') or []):
        if isinstance(err, dict) and self._walk(err.get('extensions'), arg) is not None:
          return True
      return False
    if kind == 'top':
      key, sub = arg
      v = resp.get(key)
      return isinstance(v, str) and sub.lower() in v.lower()
    if kind == 'html':
      txt = resp.get('__html__', '') if isinstance(resp, dict) else ''
      return isinstance(txt, str) and arg.lower() in txt.lower()
    if kind == 'federation':
      return (isinstance(data, dict)
              and isinstance(data.get('_service'), dict)
              and isinstance(data['_service'].get('sdl'), str)
              and len(data['_service']['sdl']) > 0)
    if kind == 'header':
      name, sub = arg
      for k, v in hdrs.items():
        if k.lower() == name.lower() and sub.lower() in str(v).lower():
          return True
      return False
    return False

  @staticmethod
  def _family_of(engine):
    for sig in SIGNALS:
      if sig[0] == engine:
        return sig[1]
    return engine

  def detect_engine(self, url, responses=None, headers=None):
    '''Score every signal and resolve engine + family + confidence.

    Returns a dict:
      { engine, family, confidence, score, signals, candidates, ambiguous,
        federation }
    or None if nothing matched.
    '''
    if responses is None or headers is None:
      responses, headers = self._send_probes(url)

    engine_score = defaultdict(int)
    engine_hits = defaultdict(list)
    engine_maxw = defaultdict(int)
    family_score = defaultdict(int)

    for sig in SIGNALS:
      if self._match(sig, responses, headers):
        engine, family, weight = sig[0], sig[1], sig[2]
        engine_score[engine] += weight
        engine_hits[engine].append(sig)
        engine_maxw[engine] = max(engine_maxw[engine], weight)
        family_score[family] += weight

    federation = any(
      self._match(('_fed', '_fed', UNIQUE, 'federation', 'federation', None), responses, headers)
      for _ in (0,)
    )

    if not engine_score:
      return None

    # Rank engines: prefer higher max-weight signal, then total score.
    ranked = sorted(engine_score.items(),
                    key=lambda kv: (engine_maxw[kv[0]], kv[1]),
                    reverse=True)
    best_engine, best_total = ranked[0]
    best_maxw = engine_maxw[best_engine]

    if best_maxw < STRONG:
      # Only family/weak evidence -> report the library family, do not
      # over-claim a specific server.
      fam = sorted(family_score.items(), key=lambda kv: kv[1], reverse=True)[0][0]
      engine = FAMILY_FALLBACK.get(fam, best_engine)
      confidence = 'low'
    else:
      engine = best_engine
      confidence = 'high' if best_maxw >= UNIQUE else 'medium'

    # Ambiguity: any OTHER engine also carrying a >=STRONG signal.
    runners = [(e, s) for e, s in ranked
               if e != best_engine and engine_maxw[e] >= STRONG]

    return {
      'engine': engine,
      'family': self._family_of(engine),
      'confidence': confidence,
      'score': best_total,
      'signals': engine_hits.get(best_engine, []),
      'candidates': ranked,
      'ambiguous': bool(runners),
      'runners': runners,
      'federation': federation,
    }
