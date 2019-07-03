@login
Feature: I want not be able to login to LITE within invalid credentials
  As a exporter
  I want to be able to login to LITE
  So that I can see my exporter dashboard

  @LT-1134_invalid
  Scenario: Login with invalid credentials
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "invalid"
    Then I see login error message
