@internal @roles
Feature: I want to create roles
  As a logged in government user
  I want to create roles with permissions
  So that I can restrict access to functionality

  @LT-1127_add
  Scenario: Create new role
    Given I go to internal homepage
    When I go to users
    And I go to manage roles
    And I add a new role called "Supervisor" with permission to "Make final decisions"
    Then I see the role in the roles list
    When I add an existing role name
    Then I see error message "Enter a name which is not already in use by another role"

  @LT-1127_empty
  Scenario: Add a role with empty field
    Given I go to internal homepage
    When I go to users
    And I go to manage roles
    And I add a new role called " " with permission to "Make final decisions"
    Then I see error message "Role name may not be blank"

  @LT-1127_over
  Scenario: Add a role with over 30 characters field
    Given I go to internal homepage
    When I go to users
    And I go to manage roles
    And I add a new role called "abcdefghijklmnopqrstuvwxyz12345" with permission to "Make final decisions"
    Then I see error message "Ensure this field has no more than 30 characters."

  @LT-1127_edit
  Scenario: Edit a role
    Given I go to internal homepage
    When I go to users
    And I go to manage roles
    And I add a new role called "Supervisor" with permission to "Make final decisions"
    And I edit my role
    Then I see the role in the roles list
