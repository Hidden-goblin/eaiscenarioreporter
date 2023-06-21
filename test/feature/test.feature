@epic=test
Feature: Test feature

  As An End User
  I want to test the reporter
  So that I will know if it's working

  !!Workflow: ../workflows/test.puml

  Background:
    Given This background is beautiful
    And I want to include it at the right level
    @id=test_1
  Scenario:
    Given I write a workflow reference
    When I generate the report
    Then The workflow picture is added