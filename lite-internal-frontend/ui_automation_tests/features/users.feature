@all @users
Feature: I want to test users

  NOTE: All these tests need to get rewritten

  @manage_users @smoke
  Scenario: Manage user
    Given I run the manage users test


  @invalid_user @regression
  Scenario: Invalid users
    Given I run the invalid user test

  @deactivate_oneself @regression
  Scenario: Deactivate oneself
    Given I run the inability to deactivate oneself test


