@compliance @all
Feature: Compliance
  As a logged in exporter user
  I want to be able to log actions required for compliance purposes
  So that I can document whether entities are complying with the law

  @skip @legacy
  Scenario: Submit and view open licence returns
    Given I go to exporter homepage and choose Test Org
    And I create an open application via api
    And I remove the flags to finalise the licence
    And I create "approve" final advice for open application
    And I create a licence for my application with "approve" decision document
    And I create a visit case for the linked compliance case
    And I produce an open licence CSV with for my licence
    When I complete an open licence return
    Then I see the success page
    When I go to my open licence returns
    Then I see my open licence return is the latest entry
    When I go to exporter homepage
    And I view my organisations compliance section
    Then I can see the compliance case in the list of cases
    When I view the compliance case
    Then I can see the contents of the compliance case
    And I can see one visit case is created
    And I view the visit case where I can see a smaller set of tabs are visible
