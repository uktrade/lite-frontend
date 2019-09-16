@queues @internal @all
Feature: I want to assign one or more specific users to a case in a work queue
  As a: Logged in government user viewing a specific work queue
  I want to: Assign an application to one or more specific users
  So that: everyone is aware which specific users are working on this case in any given work queue / department

  Background:
    Given I go to queues
    And I create application or application has been previously created
    When I enter in queue name Review
    And I go to application previously created
    And I add case to newly created queue
    And I go to the internal homepage
    And I click on the added queue in dropdown

  @LT_947_add
  Scenario: Add user to case
    When I select the checkbox for previously created case to be assigned
    And I select user to assign SSO users name
    And I click on the added queue in dropdown
    Then user is assignee on case list
    When I select the checkbox for previously created case to be assigned
    And I select user to assign SSO users name
    And I click on the added queue in dropdown
    Then user is not assignee on case list

  @LT_947_select_all
  Scenario: Select all cases and deselect
    When I click select all cases checkbox
    Then assign users button is "enabled"
    When I click select all cases checkbox
    Then assign users button is "disabled"

  @LT_947_search_filter
  Scenario: Filter by user
    When I select the checkbox for previously created case to be assigned
    And I search for SSO users name to assign
    Then only SSO users name is displayed in user list for assign cases
