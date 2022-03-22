@ecju_query @all
Feature: As a logged in exporter
I want to see when there are ECJU queries (RFIs) relating to my applications, queries and licences and be able to respond
So that I can quickly identify where action is required by me and respond to any queries

  @ecju_query
  Scenario: View and respond to a ECJU query in an application
    Given I signin and go to exporter homepage and choose Test Org
    And I submit an application with <name>,<product>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And Caseworker creates an ECJU query with "Some unique query"
    When I go to exporter homepage
    Then I see a notification next to check progress
    When I click check progress
    Then I see a notification next to the application
    When I click on my application
    Then I see a notification next to ECJU queries
    When I click the ECJU Queries tab
    Then I see "Some unique query" as the query under open queries
    When I click to respond to the ECJU query
    And I enter "Some unique response" for the response and click submit
    And I select "Confirm and send the response" and click submit
    Then I see "Some unique response" as the response under closed queries

    Examples:
    | name    | product | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |
