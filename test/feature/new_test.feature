@TF-01 @test
Feature: New Test feature

  As An End User
  I want to test the reporter
  So that I will know if it's working

  !!Workflow: ../workflows/test1.puml

  @event
  Scenario:
    Given I write a workflow reference
    When I generate the report
    Then The workflow picture is added