@all @internal @roles
Feature: I want to create roles
  As a logged in government user
  I want to create roles with permissions
  So that I can restrict access to functionality

  @LT_1127_edit @smoke
  Scenario: Edit a role
    Given I sign in to SSO or am signed into SSO
    When I go to users
    And I go to manage roles
    And I add a new role called "Supervisor" with permission to "Manage final advice" and set status to "Closed"
    And I edit my role
    Then I see the role in the roles list
