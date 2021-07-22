@all
Feature: Add a HMRC query

  @a_caseworker_test
  Scenario: Send data to HMRC
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
#    And I "approve" the open application good and country at all advice levels
#    And A template exists for the appropriate decision
    When I go to the final advice page by url
    And I remove Enforcement Check Req
    And I give advice
    And I finalise the advice
    Then I see the refused good country combination
    When I click continue
    And I click continue
    Then I see the final advice documents page
    And The decision row status is "not-started"
    When I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    Then The decision row status is "done"
    When I click continue
    And I go to application previously created
    Then The case is finalised and a document is created in the audits
    When I go to the documents tab
    Then The generated decision document is visible

  Examples:
  | name    | product | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
  | Test    | Rifle   | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and devel