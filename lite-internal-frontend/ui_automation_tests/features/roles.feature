@internal @roles
Feature: I want to create roles
  As a logged in government user
  I want to create roles with permissions
  So that I can restrict access to functionality

  @LT_1127_add
  Scenario: Create new role
    Given I go to internal homepage
    When I go to users
    And I go to manage roles
    And I add a new role called "Supervisor" with permission to "Make final decisions"
    Then I see the role in the roles list
    When I add an existing role name
    Then I see error message "Enter a name which is not already in use by another role"
    
  @LT_1127_edit
  Scenario: Edit a role
    Given I go to internal homepage
    When I go to users
    And I go to manage roles
    And I add a new role called "Supervisor" with permission to "Make final decisions"
    And I edit my role
    Then I see the role in the roles list
