# GraphQL Ruby

Source: [https://github.com/rmosolgo/graphql-ruby](https://github.com/rmosolgo/graphql-ruby)

Documentation: [https://graphql-ruby.org/](https://graphql-ruby.org/)

# Table of Contents
* [About](#About)
* [Security Features](#Security-Features)
* [Validations](#Validations)

# About
graphql-ruby is a Ruby implementation of the GraphQL specification.

# Security Features
GraphQL Ruby provides the following security features:

| Field Suggestions | Query Depth Limit | Query Cost Analysis | Automatic Persisted Queries | Introspection      | Debug Mode | Batch Requests  |
|-------------------|-------------------|---------------------|-----------------------------|--------------------|------------|-----------------|
| On by Default     | No Support        | Off by Default      | Off by Default              | Enabled by Default | No Support | On by Default   |


# Validations
GraphQL Ruby validates the following checks when a query is sent:

| Document Validations | Operation Validations | Field Validations | Argument Validations | Fragment Validations      | Value/Type Validations | Directive Validations  | Variable Validations | Misc. Validations |
|----------------------|-----------------------|-------------------|----------------------|---------------------------|--------------------------|------------------------|----------------------|-------------------|
| | [Mutation root exists](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/mutation_root_exists.rb) | [Fields are defined on type](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fields_are_defined_on_type.rb) | [Argument literals are compatible](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/argument_literals_are_compatible.rb) | [Fragment names are unique](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fragment_names_are_unique.rb) | [Input object names are unique](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/input_object_names_are_unique.rb) | [Directives are defined](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/directives_are_defined.rb) | [Variables default values are correctly typed](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/variable_default_values_are_correctly_typed.rb) | [No definitions are present](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/no_definitions_are_present.rb) |
| | [Operation names are valid](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/operation_names_are_valid.rb) | Fields have appropriate selections | Argument names are unique | Fragment spreads are possible | Required input object attributes are present | Directives are in valid locations | Variable names are unique | |
| | [Query root exists](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/query_root_exists.rb) | Field will merge | Arguments are defined | Fragment types exist | | Unique directives per location | Variable usages are allowed | |
| | [Subscription root exists](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/subscription_root_exists.rb) |  | Requried arguments are present |  Fragements are finite | | | Variables are input types | |
| | | | | Fragments are named | | | Variables are used and defined | |
| | | | | Fragments are on composite types | | | | |
