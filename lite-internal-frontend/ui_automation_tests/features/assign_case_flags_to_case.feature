@internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @LT-949_add
  Scenario: Add flag to case
    Given I create application or application has been previously created
    And I go to internal homepage
    When I go to flags
    And I add a flag called "Needs" at level "Case"
    When I go to the internal homepage
    When I click on application previously created
    And I count the number of assigned flags
    And I click edit flags link
    And I assign flags to the case
    Then Number of assigned flags has increased
    When I click edit flags link
    And I unassign flags from the case
    Then Number of assigned flags is original value
