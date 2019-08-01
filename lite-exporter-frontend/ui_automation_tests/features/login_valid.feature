@login @all
Feature:  I want to be able to login to LITE and go to dashboard
  As a exporter
  I want to be able to login to LITE
  So that I can see my exporter dashboard

  @LT_1134_valid
  Scenario: Login with valid credentials
    Given I go to exporter homepage
    Then driver title equals "Exporter hub - LITE"
