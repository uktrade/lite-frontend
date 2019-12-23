@licence @goods @filter @all
Feature: I want to search for goods in my goods list to add to an in progress application
  As a logged in exporter creating a new application
  I want to search for goods in my goods list to add to an in progress application
  So that I can quickly and easily complete my application for types of goods I have exported before

  @LT_1159_filters @regression
  Scenario: Search for goods by filters in adding preexisting good to application
    Given I go to exporter homepage and choose Test Org
    When I create a good of description "Test apple123", control code "ML4" and part number "5678" if it does not exist
    And I create a good of description "Test apple123", control code "ML4" and part number "1234" if it does not exist
    And I create a good of description "Test apple123", control code "ML5" and part number "9012" if it does not exist
    And I go to exporter homepage
    When I create a standard application
    And I click on standard goods tile
    And I click the add from organisations goods button
    And I filter by description "Test apple123" and click filter
    And I filter by control list entry "ML4" and click filter
    And I filter by part number "5678" and click filter
    Then All goods have description "Test apple123"
    And All goods have control code "ML4"
    And All goods have part number "5678"
    # Only 1 good matches all 3 criteria
    Then "1" goods are found

  @LT_1450_filters @regression
  Scenario: Search for goods by filters in goods list
    Given I go to exporter homepage and choose Test Org
    When I create a good of description "Test apple123", control code "ML4" and part number "5678" if it does not exist
    And I create a good of description "Test apple123", control code "ML4" and part number "1234" if it does not exist
    And I create a good of description "Test apple123", control code "ML5" and part number "9012" if it does not exist
    And I click on goods link
    And I filter by description "Test apple123" and click filter
    And I filter by control list entry "ML4" and click filter
    And I filter by part number "5678" and click filter
    Then All goods have description "Test apple123"
    And All goods have control code "ML4"
    And All goods have part number "5678"
    # Only 1 good matches all 3 criteria
    Then "1" goods are found