<h1 align="center">
 <img src="https://github.com/dolevf/graphw00f/blob/main/static/graphw00f.png?raw=true" height="50%" width="50%" alt="graphw00f"/>
 <br>
</h1>

<h5 align="center">
<small>Credits to <a href="https://github.com/nicholasaleks">Nick Aleks </a>for the logo!</small>
</h5>

<h1 align="center">
 graphw00f - GraphQL Server Fingerprinting
</h1>

# Table of Contents
* [How does it work?](#how-does-it-work)
* [Detections](#detections)
* [GraphQL Threat Matrix](#graphql-threat-matrix)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Configuration](#configuration)
* [Example Usage](#example)
  * [Fingerprinting GraphQL](#fingerprinting-graphql)
  * [Detecting & Fingerprinting GraphQL](#detecting-and-fingerprinting-graphql)
* [Support & Issues](#support-and-issues)
* [Resources](#resources)


# How does it work?
graphw00f (inspired by [wafw00f](https://github.com/EnableSecurity/wafw00f)) is the GraphQL fingerprinting tool for GQL endpoints, it sends a mix of benign and malformed queries to determine the GraphQL engine running behind the scenes.
graphw00f will make use of the GraphQL Threat Matrix project to provide insight into what security defences each technology provides out of the box, and whether they are on or off by default.

Specially crafted queries cause different GraphQL server implementations to respond uniquely to queries, mutations and subscriptions, this makes it trivial to fingerprint the backend engine and distinguish between the various GraphQL implementations. (CWE: [CWE-200](https://cwe.mitre.org/data/definitions/200.html))

# Detections
graphw00f currently attempts to discover the following GraphQL engines:
* Graphene - Python
* Ariadne - Python
* Apollo - TypeScript
* graphql-go - Go
* gqlgen - Go
* WPGraphQL - PHP
* GraphQL API for Wordpress - PHP
* graphql-ruby - Ruby
* graphql-php - PHP
* Hasura - Haskell
* HyperGraphQL - Java
* graphql-java - Java
* Juniper - Rust
* Sangria - Scala
* Flutter - Dart
* Diana.jl - Julia
* Strawberry - Python
* Tartiflette - Python
* Dgraph - JavaScript
* Directus - TypeScript
* AWS AppSync
* GraphQL Yoga - TypeScript
* Lighthouse - PHP
* Agoo - Ruby
* Mercurius - JavaScript
* morpheus-graphql - Haskell
* Lacinia - Clojure
* Caliban - Scala
* jaal - Golang
* absinthe-graphql - Elixir

# GraphQL Threat Matrix
The graphw00f project uses the [GraphQL Threat Matrix Project](https://github.com/nicholasaleks/graphql-threat-matrix/) as its technology security matrix database. When graphw00f successfully fingerprints a GraphQL endpoint, it will print out the threat matrix document. This document helps security engineers to identify how mature the technology is, what security features it offers, and whether it contains any CVEs.

![GraphQL Threat Matrix](/static/threat-matrix.png?raw=true "GraphQL Threat Matrix")

# Prerequisites
* python3
* requests

# Installation
## Clone Repository
`git clone https://github.com/dolevf/graphw00f.git`

## Run graphw00f
```
Usage: main.py -d -f -t http://example.com

Options:
  -h, --help            show this help message and exit
  -r, --noredirect      Do not follow redirections given by 3xx responses
  -t URL, --target=URL  target url with the path
  -f, --fingerprint     fingerprint mode
  -d, --detect          detect mode
  -p PROXY, --proxy=PROXY
                        HTTP(S) proxy URL in the form
                        http://user:pass@host:port
  -T TIMEOUT, --timeout=TIMEOUT
                        Request timeout in seconds
  -o OUTPUT_FILE, --output-file=OUTPUT_FILE
                        Output results to a file (CSV)
  -l, --list            List all GraphQL technologies graphw00f is able to
                        detect
  -u USERAGENT, --user-agent=USERAGENT
                        Custom user-agent to use (overrides the one from
                        headers configuration)
  -H HEADER, --header=HEADER
                        Custom headers to send (e.g. "Authorization: Bearer
                        ey...").
  -w WORDLIST, --wordlist=WORDLIST
                        Path to a list of custom GraphQL endpoints
  -v, --version         Print out the current version and exit.
```

# Configuration
There aren't a whole lot of configurations required for graphw00f. But, if you need things like Authorization headers or Cookies set for a particular endpoint, use the `conf.py` file.

```
# Custom Headers
HEADERS = {'User-Agent':'graphw00f'}

# Custom Cookies
COOKIES = {"PHPSESS":"DEADBEEF"}
```

Using `--user-agent` adds `User-Agent` key regardless if `conf.py` file has it, if the file already has one, command-line parameter overrides it.

# Example
## Fingerprinting GraphQL
This is an example how to fingerprint (`-f`) an endpoint where GraphQL's location is known ahead of time (`/graphql`)

```
python3 main.py -f -t https://demo.hypergraphql.org:8484/graphql

                +-------------------+
                |     graphw00f     |
                +-------------------+
                  ***            ***
                **                  ***
              **                       **
    +--------------+              +--------------+
    |    Node X    |              |    Node Y    |
    +--------------+              +--------------+
                  ***            ***
                     **        **
                       **    **
                    +------------+
                    |   Node Z   |
                    +------------+

                graphw00f - v1.0.7
          The fingerprinting tool for GraphQL
           Dolev Farhi <dolev@lethalbit.com>

[*] Checking if GraphQL is available at https://demo.hypergraphql.org:8484/graphql...
[*] Found GraphQL...
[*] Attempting to fingerprint...
[*] Discovered GraphQL Engine: (HyperGraphQL)
[!] Attack Surface Matrix: https://github.com/dolevf/graphw00f/blob/main/docs/hypergraphql.md
[!] Technologies: Java
[!] Homepage: https://www.hypergraphql.org
[*] Completed.
```

## Detecting and Fingerprinting GraphQL
This is an example how graphw00f can detect (`-d`) where GraphQL lives and then execute the fingerprinting process (`-f`).

```
python3 main.py -f -d -t http://localhost:5000

                +-------------------+
                |     graphw00f     |
                +-------------------+
                  ***            ***
                **                  ***
              **                       **
    +--------------+              +--------------+
    |    Node X    |              |    Node Y    |
    +--------------+              +--------------+
                  ***            ***
                     **        **
                       **    **
                    +------------+
                    |   Node Z   |
                    +------------+

                graphw00f - v1.1.2
          The fingerprinting tool for GraphQL
           Dolev Farhi <dolev@lethalbit.com>

[*] Checking http://dvga.example.local:5000/graphql
[!] Found GraphQL at http://dvga.example.local:5000/graphql
[*] Attempting to fingerprint...
[*] Discovered GraphQL Engine: (Graphene)
[!] Attack Surface Matrix: https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphene.md
[!] Technologies: Python
[!] Homepage: https://graphene-python.org
[*] Completed.
```

# Support and Issues
Any issues with graphw00f such as false positives, inaccurate detections, bugs, etc. please create a GitHub issue with environment details.

# Resources
Want to learn more about GraphQL? head over to my other project and hack GraphQL away: [Damn Vulnerable GraphQL Application](https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application/)
