@ecju_queries @all
Feature: As a logged in exporter
I want to see when there are ECJU queries (RFIs) relating to my applications, queries and licences and be able to respond
So that I can quickly identify where action is required by me and respond to any queries

  Scenario: view and respond to a ecju query in an application
    Given I signin and go to exporter homepage and choose Test Org
    And I submit an application with <name>,<product>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And I create an ecju query
    When I go to the recently created application with ecju query
    And I click the ECJU Queries tab
    And I click to respond to the ecju query
    And I enter "This is my response" for ecju query and click submit
    And I select "Confirm and send the response" and click submit
    Then I see my ecju query is closed

    Examples:
    | name    | product | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |
