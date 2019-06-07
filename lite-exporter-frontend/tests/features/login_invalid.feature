@exporter @login  @all
Feature: Login
As a...

  Scenario: Login with invalid credentials
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "invalid"
    Then I see login error message

