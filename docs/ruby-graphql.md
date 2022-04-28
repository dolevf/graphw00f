# Ruby GraphQL

# Table of Contents
* [About](#About)
* [Security Features](#Security-Features)

# About
ruby-graphql is a Ruby implementation of the GraphQL specification.

# Security Features
Ruby GraphQL provides the following security features:

| Field Suggestions | Query Depth Limit | Query Cost Analysis | Automatic Persisted Queries | Introspection      | Debug Mode | Batch Requests  |
|-------------------|-------------------|---------------------|-----------------------------|--------------------|------------|-----------------|
| On by Default     | No Support        | Off by Default      | Off by Default              | Enabled by Default | No Support | On by Default   |


# Validations
Ruby GraphQL validates the following checks when a query is sent:

| Document Validations | Operation Validations | Field Validations | Argument Validations | Fragment Validations      | Value/Type Validations | Directive Validations  | Variable Validations | Misc. Validations |
|----------------------|-----------------------|-------------------|----------------------|---------------------------|--------------------------|------------------------|----------------------|-------------------|
| | Mutation root exists | Fields are defined on type | Argument literals are compatible | Fragment names are unique | Input object names are unique | Directives are defined | Variables default values are correctly typed | No definitions are present |
| | Operation names are valid | Fields have appropriate selections | Argument names are unique | Fragment spreads are possible | Required input object attributes are present | Directives are in valid locations | Variable names are unique | |
| | Query root exists | Field will merge | Arguments are defined | Fragment types exist | | Unique directives per location | Variable usages are allowed | |
| | Subscription root exists |  | Requried arguments are present |  Fragements are finite | | | Variables are input types | |
| | | | | Fragments are named | | | Variables are used and defined | |
| | | | | Fragments are on composite types | | | | |
