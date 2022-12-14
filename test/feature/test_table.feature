Feature: Test feature

  As An End User
  I want to test the reporter
  So that I will know if it's working

  !!Workflow: ../workflows/test.puml

  * One rule
  * another one
  * a rule followed by a table
  | A tabular | to test |
  | --------- | ------- |
  | one| two|

  Free text in the feature description

  $ Title
  * text
  | A tabular | to test |
  | --------- | ------- |
  | one| two|

  $$ Sub title
  | A tabular | to test |
  | --------- | ------- |
  | one| two|
  | A tabular | to test |
  | one| two|

  $$ Sub title
  1. test one
  1. test two
  | A tabular | to test |
  | --------- | ------- |
  | one| two|

  Scenario:
    Given I write a workflow reference
    When I generate the report
    Then The workflow picture is added