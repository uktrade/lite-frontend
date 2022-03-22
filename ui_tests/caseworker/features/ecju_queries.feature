@all @internal @ecju_query
Feature: I want to create ECJU queries
  As a logged in government user
  I want to raise a query to an exporter about their case
  So that I can ask them for additional information or to correct an issue with the case they have submitted

  @ecju_query
  Scenario: Add an ECJU Query to a case
    # Caseworker creates query
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I click the queries tab
    And I click "Add an ECJU query"
    And I enter "Some unique query" as the query
    And I click send
    Then I see "Some unique query" as the query under open queries
    # Exporter responds to query
    When Exporter responds with "Some unique response" to the ECJU query
    # Caseworker views response
    When I go to application previously created
    And I click the queries tab
    Then I see "Some unique response" as the response under closed queries
