@all @internal @case_officer
Feature: I want to assign a dedicated case officer / single point of contact to a case
    So that all internal users and the exporter can see a single named point of contact for the case,
    and know who to contact for questions or escalation

  @skip @legacy
  Scenario: Assign and remove case officer
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click Assign Case Officer Button
    And filter by test user email
    Then I should see one user with the test user name
    When I click the user and assign
    Then I see a case officer is assigned
    When I click Assign Case Officer Button
    And I click unassign
    Then I see no case officer is assigned
