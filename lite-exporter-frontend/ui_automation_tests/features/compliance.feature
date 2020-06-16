@compliance @all
Feature: Compliance
  As a logged in exporter user
  I want to be able to log actions required for compliance purposes
  So that I can document whether entities are complying with the law

  @LT_866_submit_open_licence_returns @regression
  Scenario: Submit and view open licence returns
    Given I go to exporter homepage and choose Test Org
    And I create an open application via api
    And I remove the flags
    And I create "approve" final advice for open application
    And I create a licence for my application with "approve" decision document
    And I produce an open licence CSV with for my licence
    When I complete an open licence return
    Then I see the success page
    When I go to my open licence returns
    Then I see my open licence return is the latest entry
