<h1 align="center">
 <img src="https://github.com/dolevf/graphw00f/blob/main/static/graphw00f.png?raw=true" width="alt="graphw00f"/>
 <br>
 graphw00f - GraphQL Fingerprinting
</h1>

graphw00f (inspired by [wafw00f](https://github.com/EnableSecurity/wafw00f)) is a GraphQL fingerprinting tool. 

# How does it work?
graphw00f is a Python utility which attempts to send a mixture of benign and malformed queries to determine the GraphQL engine running behind the scenes.

Different GraphQL servers respond uniquely to queries, mutations and subscriptions given the right payload, this makes it trivial to fingerprint and distinguish between the various GraphQL servers. (CWE: [CWE-200](#CWE-Reference))

# Detections / Signatures
graphw00f currently attempts to discover the following GraphQL engines:
* Graphene
* Ariadne
* Apollo
* graphql-go
* gqlgen
* WPGraphQL
* GraphQL API for Wordpress
* Ruby GraphQL
* graphql-php
* Hasura

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
python3 graphw00f.py -t http://127.0.0.1:5000/graphql

+-------------------+           +--------------------+
|      GRAPHQL      |           |     FINGERPRINT    |
+-------------------+           +--------------------+
                  **              **                  
                    ***        ***                    
                       **    **                       
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
  
[*] Checking if GraphQL is available at http://127.0.0.1:5000/graphql...
[*] Found GraphQL.
[*] Attempting to fingerprint...
[*] Discovered GraphQL Engine!
[!] The site https://graphene-python.org is using: Graphene
[!] Language: Python
[!] Homepage: https://graphene-python.org
[*] DONE.
```
                                                                                                              
# Support and Issues
Any issues with graphw00f such as false/true positives, inaccurate detections, etc. please create a GitHub issue with environment details.

# Resources
Want to learn more about GraphQL? head over to my other project and hack GraphQL away: [Damn Vulnerable GraphQL Application](https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application/)
