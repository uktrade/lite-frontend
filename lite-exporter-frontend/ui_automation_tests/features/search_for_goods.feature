@exporter @licence @all @goods @filter
Feature: Goods
  As a...

  Scenario: Search for goods by description
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I add a good with description "Good to search" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
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

  Scenario: Search for goods by part number
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I add a good with description "Good to search" controlled "Yes" control code "1234" incorporated "Yes" and part number "999"
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

  Scenario: Remove filter
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I add a good with description "Good to search" controlled "Yes" control code "1234" incorporated "Yes" and part number "999"
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