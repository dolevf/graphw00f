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
* [GraphQL Technologies Defence Matrices](#graphql-technologies-defence-matrices)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Support & Issues](#support-and-issues)
* [Resources](#resources)


# How does it work?
graphw00f (inspired by [wafw00f](https://github.com/EnableSecurity/wafw00f)) is the GraphQL fingerprinting tool for GQL endpoints, it sends a mix of benign and malformed queries to determine the GraphQL engine running behind the scenes. 
graphw00f will provide insights into what security defences each technology provides out of the box, and whether they are on or off by default.

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
* Ruby - GraphQL
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
                                                                                           
# GraphQL Technologies Defence Matrices
Each fingerprinted technology (e.g. Graphene, Ariadne, ...) has an associated document ([example for graphene](https://github.com/dolevf/graphw00f/blob/main/docs/graphene.md)) which covers the security defence mechanisms the specific technology supports to give a better idea how the implementation may be attacked.
                                                                                                              
```
| Field Suggestions | Query Depth Limit | Query Cost Analysis | Automatic Persisted Queries | Introspection      | Debug Mode | Batch Requests  |
|-------------------|-------------------|---------------------|-----------------------------|--------------------|------------|-----------------|
| On by Default     | No Support        | No Support          | No Support                  | Enabled by Default | N/A        | Off by Default  |
```

# Prerequisites
* python3
* requests                   
                                                                                                              
# Installation
## Clone Repository
`git clone git@github.com:dolevf/graphw00f.git`

## Run graphw00f
`python3 main.py -h`

```
Usage: main.py -h

Options:
  -h, --help            show this help message and exit
  -r, --noredirect      Do not follow redirections given by 3xx responses
  -t URL, --target=URL  target url with the path
  -o OUTPUT_FILE, --output-file=OUTPUT_FILE
                        Output results to a file (CSV)
  -l, --list            List all GraphQL technologies graphw00f is able to
                        detect
  -v, --version         Print out the current version and exit.
```

# Example
```
python3 main.py -t http://127.0.0.1:5000/graphql

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

                graphw00f - v1.0.0
          The fingerprinting tool for GraphQL
  
[*] Checking if GraphQL is available at https://demo.hypergraphql.org:8484/graphql...
[*] Found GraphQL...
[*] Attempting to fingerprint...
[*] Discovered GraphQL Engine: (HyperGraphQL)
[!] Attack Surface Matrix: https://github.com/dolevf/graphw00f/blob/main/docs/hypergraphql.md
[!] Technologies: Java
[!] Homepage: https://www.hypergraphql.org
[*] Completed.
```
                                                                                                              
# Support and Issues
Any issues with graphw00f such as false positives, inaccurate detections, bugs, etc. please create a GitHub issue with environment details.

# Resources
Want to learn more about GraphQL? head over to my other project and hack GraphQL away: [Damn Vulnerable GraphQL Application](https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application/)
