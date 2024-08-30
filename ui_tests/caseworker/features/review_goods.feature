@all @internal @review_goods
Feature: I want to review, amend where required and confirm the goods ratings and descriptions on an application
  As a logged in government user
  I want to review, amend where required and confirm the goods ratings and descriptions on a standard application
  So that I can confirm the goods are correctly described

  Scenario: Gov user can add case note
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Open cases"
    And I go to my case list
    And I click on show filters
    Then I should see my case in the cases list
    When I go to application previously created
    Then I should see the product name as "Rifle" with product rating as "PL9002"
    And I click on Notes and timeline
    And I add a case note "Automated Test_Add a case note" and click Post note
    Then I should see "Automated Test_Add a case note" appear in the timeline

    Examples:
    | name    | product | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | SN-XYZ-456  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |
