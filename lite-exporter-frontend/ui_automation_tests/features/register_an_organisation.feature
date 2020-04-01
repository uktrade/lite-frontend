@exporter @all
Feature: I want to register an organisation
  As an exporter-to-be
  I want to register an organisation
  So that I can export my products in the future

  @LT_1024_register_an_organisation @regression
  Scenario: Register a commercial organisation
    Given I register but I don't belong to an organisation
    When I go to exporter homepage having logged out
    And I register a new commercial organisation
    Then I should see a success page


  @LT_1024_register_an_individual_organisation @regression
  Scenario: Register a individual organisation
    Given I register but I don't belong to an organisation
    When I go to exporter homepage having logged out
    And I register a new individual organisation
    Then I should see a success page
