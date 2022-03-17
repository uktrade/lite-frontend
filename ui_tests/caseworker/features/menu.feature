@internal @all
Feature: Go to each item in the menu

  @skip @legacy
  Scenario: Go to each item in the menu
    Given I sign in to SSO or am signed into SSO
    And I go to internal homepage
    When I refresh the page
    Then the log out link is displayed
    When I go to organisations via menu
    Then the log out link is displayed
    When I go to teams via menu
    Then the log out link is displayed
    When I go to My Team via menu
    Then the log out link is displayed
    When I go to queues via menu
    Then the log out link is displayed
    When I go to users via menu
    Then the log out link is displayed
    When I go to flags via menu
    Then the log out link is displayed
    When I go to letters via menu
    Then the log out link is displayed
