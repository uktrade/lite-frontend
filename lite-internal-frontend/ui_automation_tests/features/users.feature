@all @users
Feature: I want to test users

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

  @edit_users @smoke
  Scenario: Edit user
    Given I sign in to SSO or am signed into SSO
    And I go to users
    When I add a new user
    And I edit new user
    Then I see new user
