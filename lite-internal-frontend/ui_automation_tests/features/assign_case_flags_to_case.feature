@all @internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @LT_949_add @LT_951 @regression
  Scenario: Add flag to case
    Given I create open application or open application has been previously created
    And I go to internal homepage
    When I go to flags
    And I add a flag called UAE at level Case
    And I go to application previously created
    And I click edit flags link
    And I select previously created flag
    Then The previously created flag is assigned to the case
    When I go to the internal homepage
    Then I see previously created application
    And I see the added flags on the queue

  @LT_1185_add @LT_951 @regression
  Scenario: Add flag to good
    Given I create application or application has been previously created
    And I go to internal homepage
    When I go to flags
    And I add a flag called Suspicious at level Good
    And I go to application previously created
    And I click edit goods flags link
    And I select previously created flag
    Then the previously created goods flag is assigned to the case
    When I go to the internal homepage
    Then I see previously created application
    And I see the added flags on the queue

  @LT_951 @smoke
  Scenario: Add all flags to case
    Given I create open application or open application has been previously created
    And I go to internal homepage
    When I go to flags
    And I add a flag called Suspicious at level Good
    And I go to application previously created
    And I click edit goods flags link
    And I select previously created flag
    And I go to flags
    And I add a flag called New at level Case
    And I go to application previously created
    And I click edit flags link
    And I select previously created flag
    And I go to flags
    And I add a flag called UAE at level Case
    And I go to application previously created
    And I click edit flags link
    And I select previously created flag
    And I go to flags
    And I add a flag called Suspicious at level Organisation
    And I go to application previously created
    And I go to the organisation which submitted the case
    And I click the edit flags link
    And I select previously created flag
    And I go to the internal homepage
    Then I see previously created application
    Then I see 3 flags for the case
    When I click the expand flags dropdown
    Then I see all flags for the case

