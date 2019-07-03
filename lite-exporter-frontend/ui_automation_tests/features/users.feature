@users @all
Feature: I want to manage users
  As a logged in exporter
  I want to manage users
  So that an application/query can be managed by only active members of staff and new members of staff can be added and their details can be kept up to date

  @add_user
  Scenario: Add user
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I add user
    Then user is added

  @edit_user
  Scenario: Edit user
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I edit user then user is edited

  @deactivate
  Scenario: Deactivate user
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I deactivate user then user is deactivated

  @reactivate
  Scenario: Reactivate user
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I reactivate user then user is reactivated

  @reactivate_oneself
  Scenario: Reactivate oneself
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I try to deactivate myself I cannot
