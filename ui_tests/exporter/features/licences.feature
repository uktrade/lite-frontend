@licences @all
Feature: I want to be able to view licences as an exporter user

  Scenario: View my standard application licences
    Given I signin and go to exporter homepage and choose Test Org
    And I put the test user in the admin team
    And I create a standard application via api
    And I remove the flags to finalise the licence
    And I create "approve" final advice
    And I create a licence for my application with "approve" decision document and good decisions
    When I go to the licences page
    Then I see my standard licence
    When I view my licence
    Then I see all the typical licence details
    And I see my standard application licence details

  @skip @current
  Scenario: When a new licence is issued, an email is sent to notify LITE-HMRC
    Given I signin and go to exporter homepage and choose Test Org
    And Only my email is to be processed by LITE-HMRC
    And I put the test user in the admin team
    And I create a standard application via api
    And I remove the flags to finalise the licence
    And I create "approve" final advice
    And I create a licence for my application with "approve" decision document and good decisions
    When I go to the licences page
    Then I see my standard licence
    When I view my licence
    Then I see all the typical licence details
    And I see my standard application licence details
    And an email is sent to HMRC

  @skip @legacy
  Scenario: View my open application licences
    Given I go to exporter homepage and choose Test Org
    And I create an open application via api
    And I remove the flags to finalise the licence
    And I create "approve" final advice for open application
    And I create a licence for my open application with "approve" decision document
    When I go to the licences page
    Then I see my open licence
    When I view my licence
    Then I see all the typical licence details
    And I see my open application licence details

  @skip @legacy
  Scenario: View my mod application licences
    Given I go to exporter homepage and choose Test Org
    And an Exhibition Clearance is created
    And I create "approve" final advice
    And I create a licence for my application with "approve" decision document
    When I go to the licences page
    And I click on the clearances tab
    Then I see my exhibition licence
    When I view my licence
    Then I see all the typical licence details
    And I see my exhibition application licence details

  @skip @legacy
  Scenario: View my nlr documents
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    And I remove the flags to finalise the licence
    And I create "no_licence_required" final advice
    And I finalise my NLR decision
    When I go to the licences page
    And I click on the NLR tab
    Then I see my nlr document
