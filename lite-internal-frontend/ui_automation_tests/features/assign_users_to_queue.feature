@all @queues @internal @all @user_to_queue
Feature: I want to assign one or more specific users to a case in a work queue
  As a: Logged in government user viewing a specific work queue
  I want to: Assign an application to one or more specific users
  So that: everyone is aware which specific users are working on this case in any given work queue / department

#  Background:
#    Given I sign in to SSO or am signed into SSO
#    And I create open application or open application has been previously created
#    When I go to queues
#    When I enter in queue name Review
#    And I go to application previously created
#    And I add case to newly created queue
#    And I go to the internal homepage
#    And I click on the added queue in dropdown
#
#  @LT_947_select_all @smoke
#  Scenario: Select all cases and deselect, Add user to case
#    When I click select all cases checkbox
#    Then assign users button is "enabled"
#    When I click select all cases checkbox
#    Then assign users button is "disabled"
#    When I select the checkbox for previously created case to be assigned
#    And I select user to assign SSO users name
#    And I click on the added queue in dropdown
#    Then user is assignee on case list
#    When I filter assigned user by Not Assigned
#    Then user is not an assignee on case list
#    When I filter assigned user by SSO users name
#    Then user is assignee on case list
#    When I select the checkbox for previously created case to be assigned
#    And I select user to assign SSO users name
#    And I click on the added queue in dropdown
#    Then user is not assignee on case list
#
#  @LT_947_search_filter @regression
#  Scenario: Filter by user
#    When I select the checkbox for previously created case to be assigned
#    And I search for SSO users name to assign
#    Then only SSO users name is displayed in user list for assign cases


  @LT_1295_assign_user_to_case_and_queue @regression
  Scenario: Assign a user via a case
    Given I sign in to SSO or am signed into SSO
    And a new queue has been created
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click assign user Button
    And filter by test user email to assign a user
    Then I should see one user with the test user name
    When I click the user and click continue
    And filter by queue name
    And I click the queue and click continue
    Then I see a user is assigned

  @LT_1264_unassign_user_from_case_on_system_queue @regression
   Scenario: Unassign user from a case when visiting from a system queue
    Given I sign in to SSO or am signed into SSO
    And a new queue has been created
    And I create open application or open application has been previously created
    And I am assigned to this case on my new queue
    When I go to application previously created
    Then I see a user is assigned
    When I click I'm done
    And I unassign myself from my newly created work queue
    And I go to my work queue
    Then My case is not in the queue

  @LT_1264_unassign_user_from_case_on_work_queue @regression
   Scenario: Unassign user from a case when visiting from a work queue
    Given I sign in to SSO or am signed into SSO
    And a new queue has been created
    And I create open application or open application has been previously created
    And I am assigned to this case on my new queue
    When I go to my work queue
    And I click on my case
    Then I see a user is assigned
    When I click I'm done
    Then My case is not in the queue

  @LT_1264_mark_done_when_not_assigned_from_work_queue @regression
   Scenario: Done on case without being assigned when accessing from a work queue
    Given I sign in to SSO or am signed into SSO
    And a new queue has been created
    And I create open application or open application has been previously created
    When I go to application previously created
    And I add case to newly created queue
    And I go to my work queue
    And I click on my case
    And I click I'm done
    Then My case is not in the queue
