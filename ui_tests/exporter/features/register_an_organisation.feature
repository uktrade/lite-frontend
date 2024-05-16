# @exporter @all
# Feature: I want to register an organisation
#   As an exporter-to-be
#   I want to register an organisation
#   So that I can export my products in the future

#   @register_commercial_organisation
#   Scenario: Register a commercial organisation that is based in UK
#     When I sign in as a new user without an organisation registered
#     Then I pick an organisation "Commercial organisation"
#     And I choose the option "In the United Kingdom"
#     When I enter my information to register a commercial organisation
#     Then the organisation is registered successfully
#     And I logout

#   @register_individual_organisation
#   Scenario: Register an individual organisation that is based in UK
#     When I sign in as a new user without an organisation registered
#     Then I pick an organisation "Private individual"
#     And I choose the option "In the United Kingdom"
#     When I enter my information to register an individual organisation
#     Then the organisation is registered successfully
#     And I logout

@exporter @all
Feature: I want to register an organisation
  As an exporter-to-be
  I want to register an organisation
  So that I can export my products in the future

  @current
  Scenario: Register a commercial organisation that is based in UK
    Given I am not signed into LITE but signed into GREAT SSO
    When I sign in as user without an organisation registered
    And I enter my information from steps 1-4 to register a commercial organisation
    Then the organisation is registered successfully
    And I logout
