 @set_up  @all @users
Feature: Set up a user
As a...

  Scenario: Set up user
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on the users link
    Then I add a user
