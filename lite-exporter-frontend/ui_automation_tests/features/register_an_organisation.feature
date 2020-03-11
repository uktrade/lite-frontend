#@exporter @all
#Feature: I want to register an organisation
#  As an exporter-to-be
#  I want to register an organisation
#  So that I can export my products in the future
#
#  @LT_1024_register_an_organisation @regression
#  Scenario: Register a commercial organisation
#    Given I am logged in but I don't belong to an organisation
#    Then I should be given the option to register
#    When I click the register button
#    Then I see the option to register a commercial organisation or a private individual organisation
#    When I click commercial organisation
#    And I enter in the details for commercial organisation
#    And I enter in the details for the organisation's headquarters
#    Then I should see the summary list showing what I entered
#    When I click submit
#    Then I should see a success page
#
#  @LT_1024_register_an_organisation @regression
#  Scenario: Register a private individual organisation
#    Given I am logged in but I don't belong to an organisation
#    Then I should be given the option to register
#    When I click the register button
#    Then I see the option to register a commercial organisation or a private individual organisation
#    When I click private individual
#    And I enter in the details for the private individual
#    And I enter in the details for the organisation's headquarters
#    Then I should see the summary list showing what I entered
#    When I click submit
#    Then I should see a success page
# This test will be added/enabled when GREAT test data is available