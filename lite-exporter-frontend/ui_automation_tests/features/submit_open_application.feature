@licence @submit @all
Feature: I want to indicate the open licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1091_draft
  Scenario: Apply for a licence to draft and delete
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    Then I see the application overview
    When I delete the application

  @LT_1114
  Scenario: Submit open application
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click on the goods link from overview
    And I click Add goods type button
    And I add a good or good type with description "Sniper" controlled "Yes" control code "ML1a" incorporated "Yes" and part number "not needed"
    Then I see my goods type added at position "1" with a description and a control code
    When I click overview
    Then I see my goods type added to the overview page with a description and a control code
    When I click on the goods link from overview
    And I click Add goods type button
    And I click continue
    Then I see good types error messages
    When I add a good or good type with description "M4" controlled "Yes" control code "ML1a" incorporated "Yes" and part number "not needed"
    Then I see my goods type added at position "2" with a description and a control code
    When I click overview
    Then I see my goods type added to the overview page with a description and a control code
    When I click on countries
    Then I should see a list of countries
    When I select "Canada" from the country list
    And I select "Poland" from the country list
    And I select "United Kingdom" from the country list
    And I click continue
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1092_search
  Scenario: Search for countries
    Given I go to exporter homepage and choose Test Org
    When I go to exporter homepage
    And I click on apply for a license button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on countries
    And I search for country "Canada"
    Then only "Canada" is displayed in country list

  @LT_1363_set_countries_on_goods
  Scenario: Set countries on goods types
    Given I go to exporter homepage and choose Test Org
    When I go to exporter homepage
    And I click on apply for a license button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on the goods link from overview
    And I click Add goods type button
    And I add a good or good type with description "Sniper" controlled "Yes" control code "ML1a" incorporated "Yes" and part number "not needed"
    And I click overview
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
