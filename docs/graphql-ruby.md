# GraphQL Ruby

Language: [Ruby](https://www.ruby-lang.org/en/)

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
| :white_check_mark: On by Default     | :x: No Support        | :warning: Off by Default      | :warning: Off by Default              | :white_check_mark: Enabled by Default | :x: No Support | :white_check_mark: On by Default   |


# Validations

Total Validation Count: **28**


GraphQL Ruby validates the following checks when a query is sent:

| [Document Validations](https://spec.graphql.org/October2021/#sec-Documents) | [Operation Validations](https://spec.graphql.org/October2021/#sec-Validation.Operations) | [Field Validations](https://spec.graphql.org/October2021/#sec-Validation.Fields) | [Argument Validations](https://spec.graphql.org/October2021/#sec-Validation.Arguments) | [Fragment Validations](https://spec.graphql.org/October2021/#sec-Validation.Fragments)      | [Value/Type Validations](https://spec.graphql.org/October2021/#sec-Values) | [Directive Validations](https://spec.graphql.org/October2021/#sec-Validation.Directives)  | [Variable Validations](https://spec.graphql.org/October2021/#sec-Validation.Variables) | Misc. Validations |
|----------------------|-----------------------|-------------------|----------------------|---------------------------|--------------------------|------------------------|----------------------|-------------------|
| | [Mutation root exists](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/mutation_root_exists.rb) | [Fields are defined on type](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fields_are_defined_on_type.rb) | [Argument literals are compatible](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/argument_literals_are_compatible.rb) | [Fragment names are unique](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fragment_names_are_unique.rb) | [Input object names are unique](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/input_object_names_are_unique.rb) | [Directives are defined](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/directives_are_defined.rb) | [Variables default values are correctly typed](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/variable_default_values_are_correctly_typed.rb) | [No definitions are present](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/no_definitions_are_present.rb) |
| | [Operation names are valid](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/operation_names_are_valid.rb) | [Fields have appropriate selections](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fields_have_appropriate_selections.rb) | [Argument names are unique](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/argument_names_are_unique.rb) | [Fragment spreads are possible](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fragment_spreads_are_possible.rb) | [Required input object attributes are present](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/required_input_object_attributes_are_present.rb) | [Directives are in valid locations](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/directives_are_in_valid_locations.rb) | [Variable names are unique](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/variable_names_are_unique.rb) | |
| | [Query root exists](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/query_root_exists.rb) | [Field will merge](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fields_will_merge.rb) | [Arguments are defined](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/arguments_are_defined.rb) | [Fragment types exist](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fragment_types_exist.rb) | | [Unique directives per location](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/unique_directives_per_location.rb) | [Variable usages are allowed](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/variable_usages_are_allowed.rb) | |
| | [Subscription root exists](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/subscription_root_exists.rb) |  | [Requried arguments are present](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/required_arguments_are_present.rb) |  [Fragements are finite](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fragments_are_finite.rb) | | | [Variables are input types](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/variables_are_input_types.rb) | |
| | | | | [Fragments are named](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fragments_are_named.rb) | | | [Variables are used and defined](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/variables_are_used_and_defined.rb) | |
| | | | | [Fragments are on composite types](https://github.com/rmosolgo/graphql-ruby/blob/master/lib/graphql/static_validation/rules/fragments_are_on_composite_types.rb) | | | | |
