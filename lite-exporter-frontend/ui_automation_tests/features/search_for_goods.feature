@licence @goods @filter @all
Feature: I want to search for goods in my goods list to add to an in progress application
  As a logged in exporter creating a new application
  I want to search for goods in my goods list to add to an in progress application
  So that I can quickly and easily complete my application for types of goods I have exported before

  @LT-1159_desc
  Scenario: Search for goods by description
    Given I go to exporter homepage
    When I click on goods link
    And I click add a good button
    When I add a good or good type with description "Nickel Cadmium" controlled "Yes" control code "1234" incorporated "No" and part number "321"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on goods tile
    And I click the add from organisations goods button
    And I filter by description and click filter
    Then I see my added Good by "description"

  @LT-1159_part
  Scenario: Search for goods by part number
    Given I go to exporter homepage
    When I click on goods link
    And I click add a good button
    And I add a good or good type with description "Nickel Cadmium" controlled "Yes" control code "1234" incorporated "No" and part number "999"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on goods tile
    And I click the add from organisations goods button
    And I filter by part number and click filter
    Then I see my added Good by "part number"

  @LT-1159_remove
  Scenario: Remove filter
    Given I go to exporter homepage
    When I click on goods link
    And I click add a good button
    And I add a good or good type with description "Nickel Cadmium" controlled "Yes" control code "1234" incorporated "No" and part number "999"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on goods tile
    And I click the add from organisations goods button
    And I filter by description and click filter
    And I filter by part number and click filter
    Then I see my added Good by "part number"
    And I see my added Good by "description"
    When I remove the filters
    Then I see all goods
