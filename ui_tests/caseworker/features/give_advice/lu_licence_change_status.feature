@all @internal @change_licence_status
Feature: I want to change the license state of a licence that has been issued.
  As a logged in government user as LU Senior Manager I want to revoke a Licence that has been issued.
  Also Need to ensure that my action has been recorded in Notes and timeline

  @lu_change_licence_status
  Scenario: LU change licence status
    Given I sign in as Licensing Unit Officer
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And I prepare the application for final review
    When I go to my case list
    And I click the application previously created
    And I assign myself as case officer to the case
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I enter "reason for approving" as the reasons for approving
    And I enter "licence condition" as the licence condition
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "licence condition" as the licence condition
    And I see countersign required warning message
    When I click move case forward
    And I logout
    And I sign in as Licensing Unit Manager
    And I go to my case list
    And I click the application previously created
    And I assign myself as case adviser to the case
    And I click the recommendations and decision tab
    And I click "Review and countersign"
    And I agree with outcome and provide "licensing manager approved" as countersign comments
    And I click submit recommendation
    Then I see "licensing manager approved" as countersign comments
    When I click move case forward
    And I logout
    And I sign in as Licensing Unit Officer
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Finalise case"
    And I click save
    And I click "Generate"
    And I select the template "SIEL template"
    And I click continue
    And I click preview
    Then I see the licence number on the SIEL licence preview
    And I see that "16. Control list no" is "ML1a" on the SIEL licence preview
    When I click continue
    And I click save and publish to exporter
    And I logout
    And I sign in as Licensing Unit Senior Manager
    And I click on the "All cases" queue in dropdown
    And I click the application previously created
    And I click on "Licences" tab
    Then I see that licence status shows as "Issued"
    When I click change licence status
    And I click suspend licence and submit
    And I confirm suspending the licence
    Then I see that licence status shows as "Suspended"

    Examples:
    | name     | product | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test2    | Rifle   | SN-ABC/123  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |
