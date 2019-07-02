@exporter @login  @all
Feature: Login
As a...

  Scenario: Login with valid credentials
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    Then driver title equals "Exporter hub - LITE"