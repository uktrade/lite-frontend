@switch_org @all
Feature: I want to be able to administer applications for multiple companies
  As a consultant for export applications
  I want to be able to administer applications for multiple companies
  So that I can manage applications for all my customers

  @LT_1175 @regression
  Scenario: Switch between two organisations
    Given I have a second set up organisation
    And I go to exporter homepage and choose Test Org
    When I switch organisations to my second organisation
    Then I am on my second organisation names homepage