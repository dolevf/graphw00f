# Apollo

# Table of Contents
* [About](#About)
* [Security Features](#Security-Features)
* [Penetration Testing Tips](#Penetration-Testing-Tips)

# About
Apollo Server is a community-maintained open-source GraphQL server. It works with many Node.js HTTP server frameworks, or can run on its own with a built-in Express server. Apollo Server works with any GraphQL schema built with GraphQL.js--or define a schema's type definitions using schema definition language (SDL).
Apollo uses TypeScript as its language.

# Security Features
Apollo offers the following features

```
| Query Depth Limit                | Query Cost Analysis              | Automatic Persisted Queries | Introspection                                  | Debug Mode                                                                    | Batch Requests  |
|----------------------------------|----------------------------------|-----------------------------|------------------------------------------------|-------------------------------------------------------------------------------|-----------------|
| Supported via External Libraries | Supported via External Libraries | Supported                   | Enabled if NODE_ENV is not set to 'production' | exception.stacktrace exists if NODE_ENV is not set to 'production' or 'test'  | On by default   |
```

# Penetration Testing Tips
Unless the targeted GraphQL server developers implemented query depth limits and query cost analysis, attempt to run Denial of Service attacks such as:
  * Alias overloading
  * Field duplication
  * Deeply nested queries
