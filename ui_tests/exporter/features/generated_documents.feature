@generated_documents @all
Feature: As a logged in exporter
I want to see when there are Generated Documents relating to my applications
So that I can download the documentation

  @skip @legacy
  Scenario: view Generated Documents on an application
    Given I go to exporter homepage and choose Test Org
    And I create an open application via api
    And A document has been generated for my application
    When I go to application previously created
    And I click the Generated Documents tab
    Then I can see the Generated Document
