@all @internal @review_goods
Feature: I want to review, amend where required and confirm the goods ratings and descriptions on an application
  As a logged in government user
  I want to review, amend where required and confirm the goods ratings and descriptions on a standard application
  So that I can confirm the goods are correctly described


  @review_good
  Scenario: Gov user can review product in an application
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    When I go to application previously created
    And I select all goods
    And I click review goods
    And I input "ML1a" as the control list entry
    And I select "Yes" for is a licence required
    And I input "ARS" as annual report summary
    And I click save and continue
    And I leave control list entry field blank
    And I select this product does not have a control list entry
    And I select "No" for is a licence required
    And I input "ARS" as annual report summary
    And I click "Save and return to case details"
    Then for the first good I see "ML1a" for "Rating"
    And for the first good I see "Yes" for "Licence required"
    And for the first good I see "ARS" for "ARS"
    And for the second good I see "N/A" for "Rating"
    And for the second good I see "No" for "Licence required"
    And for the second good I see "ARS" for "ARS"

    Examples:
    | name    | product        | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle1, Rifle2 | PN-ABC-123  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |

  Scenario: Gov user can add case note
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Open cases"
    And I go to my case list
    And I click on show filters
    And I filter by application type "Standard Individual Export Licence"
    Then I should see my case in the cases list
    When I go to application previously created
    Then I should see the product name as "Rifle" with product rating as "PL9002"
    And I click on Notes and timeline
    And I add a case note "Automated Test_Add a case note" and click Post note
    Then I should see "Automated Test_Add a case note" appear in the timeline

    Examples:
    | name    | product | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | SN-XYZ-456  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |

  @skip @legacy
  Scenario: Review goods On Standard Application
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I create report summary picklist
    When I go to application previously created
    And I select good and click review
    And I respond "yes", "ML4b1", "1", "Because the good is controlled" and click submit
    Then the control list is present on the case page

  @skip @legacy
  Scenario: Review goods On Open Application
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And I create report summary picklist
    When I go to application previously created
    And I select good and click review
    And I respond "True", "ML4b1", "1", "Because the good is controlled" and click submit
    Then the control list is present on the case page
