@internal @all
Feature: Go to each item in the menu

  @verify_build @menu
  Scenario: Go to each item in the menu
    Given I go to internal homepage
    When I refresh the page
    Then I get a 200
    When I go to organisations via menu
    Then I get a 200
    When I go to teams via menu
    Then I get a 200
    When I go to My Team via menu
    Then I get a 200
    When I go to queues via menu
    Then I get a 200
    When I go to users via menu
    Then I get a 200
    When I go to flags via menu
    Then I get a 200
    When I go to letters via menu
    Then I get a 200
    When I go to HMRC via menu
    Then I get a 200
