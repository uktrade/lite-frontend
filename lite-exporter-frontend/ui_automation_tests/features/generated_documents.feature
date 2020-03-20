@generated_documents @all
Feature: As a logged in exporter
I want to see when there are Generated Documents relating to my applications
So that I can download the documentation

  @LT_1552_generated_documents @regression
  Scenario: view Generated Documents on an application
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    And A document has been generated for my application
    When I go to application previously created
    And I click the Generated Documents tab
    Then I can see the Generated Document
