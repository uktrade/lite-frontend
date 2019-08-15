@internal @ecju_query
Feature: I want to create ECJU queries
  As a logged in government user
  I want to raise a query to an exporter about their case
  So that I can ask them for additional information or to correct an issue with the case they have submitted

  @LT_1192_add
  Scenario: Add an ECJU Query to a case
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    And I create an ecju query picklist
    When I go to application previously created
    And I click the ECJU Queries button
    And I click Add an ECJU Query
    And I select a standard ECJU picklist question
    And I click continue
    Then the question text area contains expected text
    When I click back
    And I Select Write a new question
    And I click continue
    Then the question text area is empty
    When I enter text in the question text area
    And I click continue
    And I click No
    And I click continue
    Then the question text area contains previously entered text
    When I click continue
    And I click Yes
    And I click continue
    Then the new ECJU Query is visible in the list
    When I click back
    Then the ECJU Query creation is visible in the case timeline
