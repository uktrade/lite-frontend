@all @internal @ecju_query
Feature: I want to create ECJU queries
  As a logged in government user
  I want to raise a query to an exporter about their case
  So that I can ask them for additional information or to correct an issue with the case they have submitted

  @skip @legacy
  Scenario: Add an ECJU Query to a case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And I create an ecju query picklist
    When I go to application previously created
    And I go to the ECJU queries tab
    And I click new query
    And I enter in my query text
    Then the new ECJU Query is visible in the list
    And the ECJU Query creation is visible in the case timeline
    When I create a response to the ECJU query
    Then the ECJU Query is in the closed list
