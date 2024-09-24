@licences @all
Feature: I want to be able to view licences as an exporter user

  @view_standard_application_licences
  Scenario: View my standard application licences
    Given I signin and go to exporter homepage and choose Test Org
    And I put the test user in the admin team
    And I create a standard application via api
    And I assess the goods with "ML5a,ML5b"
    And I remove the flags to finalise the licence
    And I put the test user in the "Licensing Unit" team
    And I create "approve" final advice
    And I countersign the advice
    And I create a licence for my application with "approve" decision document and good decisions
    When I go to the licences page
    Then I see my standard licence
    When I view my licence
    Then I see all the typical licence details
    And I see my standard application licence details
