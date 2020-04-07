@exporter @all
Feature: I want to register an organisation
  As an exporter-to-be
  I want to register an organisation
  So that I can export my products in the future


  #NOTE : These are tagged with @final because they need to get run at the end.
  @LT_1024_register_an_organisation @final
  Scenario: Register a commercial organisation
    Given I am not logged in
    And I register but I don't belong to an organisation
    When I sign as user without an organisation registered
    And I register a new commercial organisation
    Then I should see a success page


  @LT_1024_register_an_individual_organisation @final
  Scenario: Register a individual organisation
    Given I am not logged in
    And I register but I don't belong to an organisation
    When I sign as user without an organisation registered
    And I register a new individual organisation
    Then I should see a success page
