@licence @goods @filter @all
Feature: I want to search for goods in my goods list to add to an in progress application
  As a logged in exporter creating a new application
  I want to search for goods in my goods list to add to an in progress application
  So that I can quickly and easily complete my application for types of goods I have exported before

  @skip @legacy
  Scenario: Search for goods by filters in goods list
    Given I go to exporter homepage and choose Test Org
    When I create a good
    And I click on goods link
    And I filter by the good's description and click filter
    Then all goods have the description
    When I filter by the good's control list entry and click filter
    Then all goods have the control list entry
    When I filter by the good's part number and click filter
    Then all goods have the part number
    And only one good matches the filters
