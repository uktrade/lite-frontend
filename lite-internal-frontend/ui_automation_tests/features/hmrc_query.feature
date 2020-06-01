@all
Feature: Add a HMRC query

  @regression @HMRC
  Scenario: Add a HMRC query
    Given I sign in to SSO or am signed into SSO
    And I create HMRC query
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
