@all @queues @internal @all @user_to_queue
Feature: I want to assign one or more specific users to a case in a work queue
  As a: Logged in government user viewing a specific work queue
  I want to: Assign an application to one or more specific users
  So that: everyone is aware which specific users are working on this case in any given work queue / department


  @skip @legacy
  Scenario: Select all cases and deselect, Add user to case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to queues
    And I add a new queue
    And I go to application previously created
    And I add case to newly created queue
    And I go to the internal homepage
    And I click on the added queue in dropdown
    Then assign users button is "disabled"
    When I click select all cases checkbox
    Then assign users button is "enabled"
    When I click select all cases checkbox
    And I select the checkbox for previously created case to be assigned
    And I select user to assign SSO users name
    Then user is assignee on case list
    When I filter assigned user by Not Assigned
    Then my case is not in the queue
    When I click clear filters
    When I select the checkbox for previously created case to be assigned
    And I select user to assign SSO users name
    And I click on the added queue in dropdown
    Then user is not assignee on case list


  @skip @legacy
  Scenario: Filter by user
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to queues
    And I add a new queue
    And I go to application previously created
    And I add case to newly created queue
    And I go to the internal homepage
    And I click on the added queue in dropdown
    And I select the checkbox for previously created case to be assigned
    And I search for SSO users name to assign
    Then only SSO users name is displayed in user list for assign cases


  @skip @legacy
  Scenario: Assign a user via a case
    Given I sign in to SSO or am signed into SSO
    And a queue has been created
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click assign user Button
    And filter by test user email to assign a user
    Then I should see one user with the test user name
    When I click the user and click continue
    And filter by queue name
    And I click the queue and click continue
    Then I see a user is assigned

  @skip @legacy
   Scenario: Unassign user from a case when visiting from a system queue
    Given I sign in to SSO or am signed into SSO
    And a queue has been created
    And I create open application or open application has been previously created
    And I am assigned to this case on my new queue
    When I go to application previously created
    Then I see a user is assigned
    When I click I'm done
    And I unassign myself from my newly created work queue
    And I go to my work queue
    Then my case is not in the queue

  @skip @legacy
   Scenario: Unassign user from a case when visiting from a work queue
    Given I sign in to SSO or am signed into SSO
    And a queue has been created
    And I create open application or open application has been previously created
    And I am assigned to this case on my new queue
    When I go to my work queue
    And I click on my case
    Then I see a user is assigned
    When I click I'm done
    And I unassign myself from all queues
    And I go to my work queue
    Then my case is not in the queue

  @skip @legacy
   Scenario: Done on case without being assigned when accessing from a work queue
    Given I sign in to SSO or am signed into SSO
    And a queue has been created
    And I create open application or open application has been previously created
    When I go to application previously created
    And I add case to newly created queue
    And I go to my work queue
    And I click on my case
    And I click I'm done
    And I unassign myself from all queues
    And I go to my work queue
    Then my case is not in the queue
