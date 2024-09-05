@all @internal @view_queue_view
Feature: I want to view cases in the queue view
  As a Logged in government user
  I want to view cases in the queue view
  So that I can make review the case before making any decisions

  Scenario: Gov user can see case in queue view
    Given I sign in as Test UAT user
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to the case list page
    Then I should see my case in the cases list

    Examples:
    | name    | product | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | PN-123/XYZ  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |

  Scenario: Gov user can customise queue view
    Given I sign in as Test UAT user
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to the case list page
    Then I should be able to customise the queue view

    Examples:
    | name    | product | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | PN-123/XYZ  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |
