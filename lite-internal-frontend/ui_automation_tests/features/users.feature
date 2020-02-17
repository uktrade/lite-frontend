@all @users
Feature: I want to test users

  NOTE: I run the manage users test needs to get edited to just do edit user.

  @deactivate_user @regression
  Scenario: Add user, deactivate then reactivate
    Given I sign in to SSO or am signed into SSO
    And I go to users
    When I add a new user
    And I show filters
    And filter status has been changed to "Active"
    Then I see new user
    When filter status has been changed to "All"
    Then I see new user
    When I deactivate new user
    When I show filters
    And filter status has been changed to "Active"
    Then I dont see new user
    When filter status has been changed to "All"
    Then I see new user
    When I reactivate new user
    And I show filters
    And filter status has been changed to "Active"
    Then I see new user
    When filter status has been changed to "All"
    Then I see new user

  @manage_users @smoke
  Scenario: Manage user
    Given I run the manage users test
