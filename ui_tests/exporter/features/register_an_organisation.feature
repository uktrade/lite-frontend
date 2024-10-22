@exporter @all
Feature: I want to register an organisation
  As an exporter-to-be
  I want to register an organisation
  So that I can export my products in the future

  @register_commercial_organisation
  Scenario: Register a commercial organisation that is based in UK
    Given I make sure that I am not logged in
    When I sign in as a new user without an organisation registered
    Then I choose the Commercial organisation and continue
    Then I choose the option In the United Kingdom and submit
    When I enter company name
    And I enter company EORI number
    And I enter company SIC number
    And I enter company VAT number
    And I enter registration number and continue
    And I enter random site details and finish submitting
    Then the organisation is registered successfully
    Then I logout

  @register_individual_organisation
  Scenario: Register an individual organisation that is based in UK
    Given I make sure that I am not logged in
    When I sign in as a new user without an organisation registered
    Then I choose the Private invidual and continue
    Then I choose the option In the United Kingdom and submit
    When I enter company name
    And I enter company EORI number
    And I enter registration number and continue
    And I enter random site details and finish submitting
    Then the organisation is registered successfully
    Then I logout
