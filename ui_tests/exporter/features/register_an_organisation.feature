@exporter @all
Feature: I want to register an organisation
  As an exporter-to-be
  I want to register an organisation
  So that I can export my products in the future

  @skip @current
  Scenario: Register a commercial organisation that is based in UK
    Given I am not signed into LITE but signed into GREAT SSO
    When I sign in as user without an organisation registered
    And I enter my information from steps 1-4 to register a commercial organisation
    Then the organisation is registered successfully
    And I logout
