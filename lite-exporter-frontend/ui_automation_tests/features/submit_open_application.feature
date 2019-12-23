@licence @submit @all @open
Feature: I want to indicate the open licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1091_draft @regression
  Scenario: Apply for a licence to draft and delete
    Given I go to exporter homepage and choose Test Org
    When I create an open application
    Then I see the application overview
    When I delete the application

  @LT_1114 @submit_open_application @LT_1092_search @smoke
  Scenario: Submit open application
    Given I go to exporter homepage and choose Test Org
    When I create an open application
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I click on the goods link from overview
    And I click Add goods type button
    And I add a good or good type with description "Sniper" controlled "Yes" control code "ML1a" incorporated "Yes" and part number "not needed"
    Then I see my goods type added at position "1" with a description and a control code
    When I click the back link
    Then I see my goods type added to the overview page with a description and a control code
    When I click on the goods link from overview
    And I click Add goods type button
    And I click continue
    Then I see good types error messages
    When I add a good or good type with description "M4" controlled "Yes" control code "ML1a" incorporated "Yes" and part number "not needed"
    Then I see my goods type added at position "2" with a description and a control code
    When I click the back link
    Then I see my goods type added to the overview page with a description and a control code
    When I click on countries
    Then I should see a list of countries
    When I select "Canada" from the country list
    And I select "Poland" from the country list
    And I select "United Kingdom" from the country list
    And I click select all countries
    Then all checkboxes are selected
    When I search for country "Canada"
    Then only "Canada" is displayed in country list
    When I click continue
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1363_set_countries_on_goods @regression
  Scenario: Set countries on goods types
    Given I go to exporter homepage and choose Test Org
    When I go to exporter homepage
    When I create an open application
    And I click on the goods link from overview
    And I click Add goods type button
    And I add a good or good type with description "Sniper" controlled "Yes" control code "ML1a" incorporated "Yes" and part number "not needed"
    When I click the back link
    And I click on countries
    And I select "Poland" from the country list
    And I select "United Kingdom" from the country list
    And I click continue
    And I click on assign countries to goods
    And I "assign" all countries to all goods
    Then I see all countries are "assigned" to all goods
    When I click on assign countries to goods
    And I "unassign" all countries to all goods
    Then I see all countries are "unassigned" to all goods
    When I click on assign countries to goods
    And I "assign" all countries to all goods with link
    Then I see all countries are "assigned" to all goods
    When I click on assign countries to goods
    And I "unassign" all countries to all goods with link
    Then I see all countries are "unassigned" to all goods
