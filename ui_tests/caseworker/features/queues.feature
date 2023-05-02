@all @internal @queues
Feature: I want to define new work queues and the teams they belong to
  As a logged in government user
  I want to be able to define new work queues and the department they belong to
  So that new government departments and teams within departments which require their own work queues can easily have one

@all @internal @queues
Feature: I want to view all cases ready to review
  As a logged in government user
  I want to see how many open cases there are
  So that I can quickly make an assessement

  Scenario: Go to work queue
    Given I sign in to SSO or am signed into SSO
    When I go to the internal homepage
    Then I see the all cases tab
    And I see the open queries tab
    And I see the my cases tab
