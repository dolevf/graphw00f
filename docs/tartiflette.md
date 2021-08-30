# Tartiflette

# Table of Contents
* [About](#About)
* [Security Features](#Security-Features)

# About
Tartiflette is a library for building GraphQL APIs in Python, built with Python 3.6+

# Security Features
Tartiflette offers the following features:

```
| Field Suggestions | Query Depth Limit | Query Cost Analysis | Automatic Persisted Queries | Introspection      | Debug Mode | Batch Requests  |
|-------------------|-------------------|---------------------|-----------------------------|--------------------|------------|-----------------|
| No Support        | No Support        | No Support          | No Support                  | Enabled by Default | N/A        | No Support      |
```

Despite Tartiflette not having basic security support, it does provide [rate limits on a per field basis](https://tartiflette.io/docs/tutorial/rate-limit-fields-with-directives).
