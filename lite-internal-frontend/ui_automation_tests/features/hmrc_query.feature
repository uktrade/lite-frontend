@all
Feature: Add a HMRC query

  @smoke @HMRC
  Scenario: Add a HMRC query
    Given I sign in to SSO or am signed into SSO
    And I create HMRC query
    When I go to the case
    Then I see HMRC query

