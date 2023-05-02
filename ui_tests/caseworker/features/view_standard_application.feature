@all @internal @view_cases
Feature: I want to view the case details of a case
  As a Logged in government user
  I want to view the details on a case
  So that I can make review the case before making any decisions

  Scenario: Gov user can view product document
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to the case list page
    And I click on show filters
    And I filter by application type "Standard Individual Export Licence"
    Then I should see my case in the cases list
    When I go to application previously created
    And I click on "Documents" tab
    Then I should see a link to download the document

    Examples:
    | name    | product | part_number  | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | SN-PN-123/AB | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |
