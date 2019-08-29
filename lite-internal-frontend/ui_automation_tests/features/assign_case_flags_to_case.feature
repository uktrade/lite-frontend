@internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @LT_949_add
  Scenario: Add flag to case
    Given I create application or application has been previously created
    And I go to flags
    When I add a flag called UAE at level Case
    And I go to application previously created
    And I click edit flags link
    And I select previously created flag
    Then The previously created flag is assigned to the case
