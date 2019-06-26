@internal @queues @LT-919

Feature: I want to define new work queues and the teams they belong to
  As a logged in government user
  I want to be able to define new work queues and the department they belong to
  So that new government departments and teams within departments which require their own work queues can easily have one


  @LT-919_add
  Scenario: Add and edit a new queue
    Given I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name "New Queue"
    Then I see the new queue
    When I go to the internal homepage
    And I click on new queue in dropdown

  @LT-919_edit
  Scenario: Edit a new queue
    Given I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name "To Edit"
    And I edit the new queue
    Then I see the new queue
    When I go to the internal homepage
    And I click on new queue in dropdown

  @LT-919_empty_validation
  Scenario: Add empty queue
    Given I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name " "
    Then I see error message "This field may not be blank."