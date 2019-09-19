@internal @roles
Feature: I want to create roles
  As a logged in government user
  I want to create roles with permissions
  So that I can restrict access to functionality

  @LT_1127_edit
  Scenario: Edit a role
    Given I go to internal homepage
    When I go to users
    And I go to manage roles
    And I add a new role called "Supervisor" with permission to "Manage final advice"
    And I edit my role
    Then I see the role in the roles list
