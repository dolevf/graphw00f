# Hasura

# Table of Contents
* [About](#About)
* [Security Features](#Security-Features)

# About
The Hasura GraphQL engine makes your data instantly accessible over a real-time GraphQL API, so you can build and ship modern apps and APIs faster. Hasura connects to your databases, REST servers, GraphQL servers, and third party APIs to provide a unified realtime GraphQL API across all your data sources.

# Security Features
While Hasura Cloud provides some security mechanisms, Hasura API (the non-cloud version) provides a limited set of security features:

```
| Field Suggestions | Query Depth Limit | Query Cost Analysis | Automatic Persisted Queries | Introspection | Debug Mode | Batch Requests  |
|-------------------|-------------------|---------------------|-----------------------------|---------------|------------|-----------------|
| On by Default     | No Support        | No Support          | No Support                  | N/A           | No Support | No Support      |
```

Hasura non-cloud provides Access Control Lists options, however, they must be explicitly enabled and used.