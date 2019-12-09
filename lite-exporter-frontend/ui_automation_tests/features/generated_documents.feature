@generated_documents @all
Feature: As a logged in exporter
I want to see when there are Generated Documents relating to my applications
So that I can download the documentation

  @LT_1552_generated_documents @smoke
  Scenario: view Generated Documents on an application
    Given I go to exporter homepage and choose Test Org
    When I go to the recently created application with a Generated Document attached
    And I click the Generated Documents tab
    Then I can see the Generated Document
