@users @all
Feature: I want to manage users
  As a logged in exporter
  I want to manage users
  So that an application/query can be managed by only active members of staff and new members of staff can be added and their details can be kept up to date

  @LT_937_setup
  Scenario: Set up user
    Given I go to exporter homepage
    When I click on the users link
    Then I add a user

  @add_user
  Scenario: Add user
    Given I go to exporter homepage
    When I add user
    Then user is added

  @edit_user
  Scenario: Edit user
    Given I go to exporter homepage
    When I edit user then user is edited

#  @deactivate
#  Scenario: Deactivate user
#    Given I go to exporter homepage
#    When I add the second test user
#    And I deactivate user then user is deactivated
#    And I go to exporter homepage
#    And I reactivate user then user is reactivated

  @reactivate_oneself
  Scenario: Reactivate oneself
    Given I go to exporter homepage
    When I try to deactivate myself I cannot
