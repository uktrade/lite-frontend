@all @internal @queues
Feature: I want to define new work queues and the teams they belong to
  As a logged in government user
  I want to be able to define new work queues and the department they belong to
  So that new government departments and teams within departments which require their own work queues can easily have one

  @skip @legacy
  Scenario: Add and edit a queue
    Given I sign in to SSO or am signed into SSO
    When I go to queues
    And I add a new queue
    Then I see my queue
    When I edit the new queue
    Then I see my queue
    When I go to the internal homepage
    And I click on edited queue in dropdown

  @skip @legacy
  Scenario: Move case to new queue and remove from new queue
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to queues
    And I add a new queue
    And I go to application previously created
    And I add case to newly created queue
    Then I see at least "1" queue checkboxes selected
    When I go to the internal homepage
    And I click on new queue in dropdown
    Then I see previously created application
    When I go to application previously created
    Then queue change is in audit trail

  @skip @legacy
  Scenario: Closed cases appear on the all cases queue
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click change status
    And I select status "Withdrawn" and save
    And I go to the internal homepage
    And I click on the "All cases" queue in dropdown
    Then I see previously created application

  @skip @legcay
  Scenario: Closed cases dont appear on the open cases queue
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click change status
    And I select status "Withdrawn" and save
    And I go to the internal homepage
    And I click on the "Open cases" queue in dropdown
    Then I don't see previously created application

  @skip @legacy
  Scenario: Finish with a team queue and have countersigning queue automatically apply
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And a queue has been created
    And a new countersigning queue has been created
    When I go to queues
    Then I see my queue
    When I edit the new queue with a countersigning queue
    Then I see my queue in the list with a countersigning queue
    When I go to application previously created
    And I add case to newly created queue
    And I go to application previously created for my queue
    And I click I'm done
    And I click continue
    And I go to my work queue
    Then my case is not in the queue
    When I go to the countersigning queue
    Then I should see my case in the cases list
