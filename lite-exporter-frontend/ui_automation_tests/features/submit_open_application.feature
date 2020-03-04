@licence @submit @all @open
Feature: I want to indicate the open licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1114 @submit_open_application @LT_1092_search @smoke
  Scenario: Submit open application
    Given I go to exporter homepage and choose Test Org
    When I create an open application
    And I click on the "location" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I click on the "goods" section
    And I add a goods type with description "Sniper" controlled "Yes" control code "ML1a" incorporated "Yes"
    Then I see my goods type added at position "1" with a description and a control code
    When I click the back link
    When I click on the "countries" section
    Then I should see a list of countries
    When I select "Canada" from the country list
    And I click select all countries
    Then all checkboxes are selected
    When I search for country "Canada"
    Then only "Canada" is displayed in country list
    When I click continue
    And I click on the "countries-matrix" section
    When I "unassign" all countries to all goods with link
    Then I see all countries are "unassigned" to all goods
    When I "assign" all countries to all goods with link
    Then I see all countries are "assigned" to all goods
    When I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click on applications
    Then I see submitted application
