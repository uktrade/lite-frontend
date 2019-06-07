@exporter @licence @all @goods @filter
Feature: Goods
  As a...

  Scenario: Search for goods by description
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on goods link
    When I add a good with description "Good to search" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
    When I go to exporter homepage
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click on goods tile
    When I click the add from organisations goods button
    When I filter by description and click filter
    Then I see my added Good by "description"

  Scenario: Search for goods by part number
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on goods link
    When I add a good with description "Good to search" controlled "Yes" control code "1234" incorporated "Yes" and part number "999"
    When I go to exporter homepage
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click on goods tile
    When I click the add from organisations goods button
    When I filter by part number and click filter
    Then I see my added Good by "part number"

  Scenario: Remove filter
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on goods link
    When I add a good with description "Good to search" controlled "Yes" control code "1234" incorporated "Yes" and part number "999"
    When I go to exporter homepage
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click on goods tile
    When I click the add from organisations goods button
    When I filter by description and click filter
    When I filter by part number and click filter
    Then I see my added Good by "part number"
    Then I see my added Good by "description"
    When I remove the filters
    Then I see all goods