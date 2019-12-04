@roles @all
Feature: I want to create roles
  As a logged in exporter user with permission to administer roles
  I want to create roles with permissions
  So that I can restrict access to functionality

  @LT_1400_edit @smoke
  Scenario: Edit a role
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    And I go to manage roles
    And I add a new role called "Supervisor" with permission to "Administer users"
    And I edit my role
    Then I see the role in the roles list
