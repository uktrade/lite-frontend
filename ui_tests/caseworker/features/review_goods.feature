@all @internal @review_goods
Feature: I want to review, amend where required and confirm the goods ratings and descriptions on an application
  As a logged in government user
  I want to review, amend where required and confirm the goods ratings and descriptions on a standard application
  So that I can confirm the goods are correctly described


  Scenario: Gov user can review product in an application
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to my profile page
    And I change my team to "TAU" and default queue to "Open cases"
    And I go to my case list
    And I click on show filters
    And I filter by application type "Standard Individual Export Licence"
    Then I should see my case in the cases list
    When I go to application previously created
    Then I should see the product name as "Rifle" with product rating as "PL9002"
    And I select the product and click on Review goods
    And I update the control list entry to "ML4b"
    And I input "Rifles" for annual report summary and submit
    Then I should see the product name as "Rifle" with product rating as "ML4b"
    And the product status is "Verified"

    Examples:
    | name    | product | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |

  @skip @LT_1300 @regression
  Scenario: Review goods On Standard Application
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I create report summary picklist
    When I go to application previously created
    And I select good and click review
    And I respond "yes", "ML4b1", "1", "Because the good is controlled" and click submit
    Then the control list is present on the case page

  @skip @LT_1629 @regression
  Scenario: Review goods On Open Application
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And I create report summary picklist
    When I go to application previously created
    And I select good and click review
    And I respond "True", "ML4b1", "1", "Because the good is controlled" and click submit
    Then the control list is present on the case page
