@licence @submit @all @open
Feature: I want to indicate the open licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1114 @submit_open_application @LT_1092_search @smoke
  Scenario: Submit open application
    Given I go to exporter homepage and choose Test Org
    When I create an open application of a "permanent" export type
    And I click on the "location" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I click on the "end_use_details" section
    And I provide details of the intended end use of the products
    And I answer "Yes" for informed by ECJU to apply
    And I answer "No" for informed by ECJU about WMD use
    And I answer "Yes" for suspected WMD use
    And I save and continue on the summary page
    And I click on the "route_of_goods" section
    And I answer "Yes" for shipping air waybill or lading
    And I click continue
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
    And I agree to the declaration
    Then application is submitted
    When I go to exporter homepage
    And I click on applications
    Then I see submitted application

  @LT_1758_open_temporary_application_with_temporary_export_details @regression
  Scenario: Submit open application
    Given I go to exporter homepage and choose Test Org
    When I create an open application of a "temporary" export type
    And I click on the "location" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I click on the "end_use_details" section
    And I provide details of the intended end use of the products
    And I answer "Yes" for informed by ECJU to apply
    And I answer "No" for informed by ECJU about WMD use
    And I answer "Yes" for suspected WMD use
    And I save and continue on the summary page
    And I click on the "temporary_export_details" section
    And I provide details of why my export is temporary
    And I answer "No" for whether the products remain under my direct control
    And I enter the date "27", "03", "2026" when the products will return to the UK
    And I save and continue on the summary page
    And I click on the "route_of_goods" section
    And I answer "Yes" for shipping air waybill or lading
    And I click continue
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
