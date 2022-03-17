@all @internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @skip @legacy
  Scenario: Add all flags to case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And all types of flags exist
    When I go to application previously created
    And I click edit flags on the first good
    And I select a "Good" flag
    And I click edit flags link
    And I select a "Case" flag
    And I click edit flags on the first destination
    And I select a "Destination" flag
    And I go to application previously created
    And I go to the organisation which submitted the case
    And I click the edit flags link
    And I select a "Organisation" flag
    Then the "added" flag appears in the audit trail
    When I go to application previously created
    Then I see added flags to case in case view
    #rollback
    When I go to application previously created
    And I click edit flags on the first good
    And I deselect a "Good" flag
    And I click edit flags link
    And I deselect a "Case" flag
    And I click edit flags on the first destination
    And I deselect a "Destination" flag
    And I go to application previously created
    And I go to the organisation which submitted the case
