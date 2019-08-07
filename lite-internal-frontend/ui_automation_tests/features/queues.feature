@internal @queues
Feature: I want to define new work queues and the teams they belong to
  As a logged in government user
  I want to be able to define new work queues and the department they belong to
  So that new government departments and teams within departments which require their own work queues can easily have one


  @LT_919_add
  Scenario: Add a new queue
    Given I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name "Ready for Review"
    Then I see the new queue
    When I go to the internal homepage
    And I click on new queue in dropdown

  @LT_919_edit
  Scenario: Edit a new queue
    Given I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name "Ready for Edit"
    And I edit the new queue
    Then I see the new queue

  @LT_919_empty_validation
  Scenario: Add empty queue
    Given I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name " "
    Then I see error message "Give the queue a valid name"

  @LT_1125_move_cases
  Scenario: Move case to new queue and remove from new queue
    Given I create application or application has been previously created
    And I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name "Queue to move case to"
    And I go to application previously created
    And I add case to new queue
    And I go to the internal homepage
    And I click on new queue in dropdown
    Then I see previously created application
    When I go to application previously created
    And I move case to new cases original queue and remove from new queue
    And I go to the internal homepage
    And I click on new queue in dropdown
    Then there are no cases shown

  @LT_1125_error
  Scenario: Move cases error message when not selecting any queues
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I deselect all queues
    Then I see error message "Select at least one queue"

  @LT-1123-view_all_cases @view_all_cases
  Scenario: All cases appear on the all cases queue
    Given I create application or application has been previously created
    And I go to internal homepage
    When I click on the "All cases" queue in dropdown
    Then I see previously created application

  @LT-1123-view_all_cases @view_all_cases
  Scenario: Open cases appear on the open cases queue
    Given I create application or application has been previously created
    And I go to internal homepage
    When I click on the "Open cases" queue in dropdown
    Then I see previously created application

  @LT-1123-view_all_cases @view_all_cases
  Scenario: Closed cases appear on the all cases queue
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click progress application
    And I select status "Withdrawn" and save
    And I go to the internal homepage
    And I click on the "All cases" queue in dropdown
    Then I see previously created application

  @LT-1123-view_all_cases @view_all_cases
  Scenario: Closed cases dont appear on the open cases queue
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click progress application
    And I select status "Withdrawn" and save
    And I go to the internal homepage
    And I click on the "Open cases" queue in dropdown
    And I refresh the page
    Then I dont see previously created application

  @LT_1125_move_cases_clc_query
  Scenario: Move CLC Query to different queue
    Given I create clc query or clc query has been previously created
    And I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name "Queue to move case to"
    And I go to application previously created
    And I add case to new queue
    And I go to the internal homepage
    And I click on new queue in dropdown
    And I click on the clc-case previously created
    And I move case to new cases original queue and remove from new queue
    And I go to the internal homepage
    And I click on new queue in dropdown
    Then there are no cases shown
