@licence @goods @filter @all
Feature: I want to search for goods in my goods list to add to an in progress application
  As a logged in exporter creating a new application
  I want to search for goods in my goods list to add to an in progress application
  So that I can quickly and easily complete my application for types of goods I have exported before

  @LT_1159_filters
  Scenario: Search for goods by filters
    Given I go to exporter homepage and choose Test Org
    When I create a good of description "Test apple123", control code "ML4" and part number "5678" if it does not exist
    And I create a good of description "Test apple123", control code "ML4" and part number "1234" if it does not exist
    And I create a good of description "Test apple123", control code "ML5" and part number "9012" if it does not exist
    And I go to exporter homepage
    And I click on apply for a license button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on goods tile
    And I click the add from organisations goods button
    And I filter by description "Test apple123" and click filter
    And I filter by control list entry "ML4" and click filter
    And I filter by part number "5678" and click filter
    Then All goods have description "Test apple123"
    And All goods have control code "ML4"
    And All goods have part number "5678"
    # Only 1 good matches all 3 criteria
    And "1" goods are found
    When I remove the part number filter
    Then All goods have description "Test apple123"
    And All goods have control code "ML4"
    # 2 test goods match these criteria
    And "2" goods are found
    When I remove the control code filter
    Then All goods have description "Test apple123"
    # All test goods match these criteria
    And "3" goods are found
    When I remove the description filter
    Then I see all goods
