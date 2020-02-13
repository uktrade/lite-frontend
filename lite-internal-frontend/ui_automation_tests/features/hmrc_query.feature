@all
Feature: Add a HMRC query

  @smoke @HMRC
  Scenario: Add a HMRC query
    Given I sign in to SSO or am signed into SSO
    Given I go to internal homepage
    When I show filters
    When filter case type has been changed to "HMRC Query"
    When I go to HMRC query
    Then I see HMRC query

