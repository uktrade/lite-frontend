@set_up @users
Feature:  I want to manage users
  As a logged in exporter
  I want to manage users
  So that an application/query can be managed by only active members of staff and new members of staff can be added and their details can be kept up to date

  @LT-937_setup
  Scenario: Set up user
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on the users link
    Then I add a user
