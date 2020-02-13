@all
Feature: Add a HMRC query

  @smoke @HMRC
  Scenario: Add a HMRC query
    Given I sign in to SSO or am signed into SSO
    And I create HMRC query
    And I go to internal homepage
    When I go to HMRC query previously created
    Then I see HMRC query

