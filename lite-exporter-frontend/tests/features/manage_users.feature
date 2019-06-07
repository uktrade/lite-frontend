 @set_up  @all @users
Feature: Manage users
As a...

  Scenario: Add a user and edit user
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on users
    When I add a new user
    Then I see the manage user screen
    When I click edit user
