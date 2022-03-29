@all @internal @enforcement
Feature: I want to export and import XML for enforcement checking
  As a logged in government user
  I want to download the entities for all application cases on a queue in XML format
  So that I can upload it to an entity checking system to look for a match


  Scenario: Export cases on a work queue that need enforcement check
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to application previously created
    And I assign the case to "Enforcement Unit Cases to Review" queue
    When I go to my profile page
    And I change my team to "Enforcement Unit" and default queue to "Enforcement Unit Cases to Review"
    And I go to my case list
    And I cleanup the temporary files created
    When I click export enforcement xml
    And I go to application previously created
    Then the file "enforcement_check.xml" is downloaded
    And the downloaded file should include "CONSIGNEE" "COUNTRY" as "Belgium"
    And the downloaded file should include "CONSIGNEE" "PD_SURNAME" as "Automated Consignee"
    And the downloaded file should include "CONSIGNEE" "ADDRESS1" as "1234, Trade centre"
    And the downloaded file should include "END_USER" "COUNTRY" as "Belgium"
    And the downloaded file should include "END_USER" "PD_SURNAME" as "Automated End user"
    And the downloaded file should include "END_USER" "ADDRESS1" as "1234, High street"
    And I remove the case from "Enforcement Unit Cases to Review" queue

    Examples:
    | name    | product | part_number | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  |
    | Test    | Rifle   | SN-ABC/123  | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development |

  Scenario: Import xml file after enforcement checks
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And the status is set to "submitted"
    When I go to application previously created
    And I assign the case to "Enforcement Unit Cases to Review" queue
    When I go to my profile page
    And I change my team to "Enforcement Unit" and default queue to "Enforcement Unit Cases to Review"
    And I go to my case list
    And I cleanup the temporary files created
    And I click "Export EU XML"
    Then an XML file is downloaded onto my device
    When I include "END_USER" details and generate import file
    Then for FLAG the file has "N"
    And for "CODE1" the file has the "END_USER" data "ELA_ID" number from export file
    And for "CODE2" the file has the "END_USER" data "SH_ID" number from export file
    When I go to my case list
    And I click "Import EU XML"
    And I attach the file above
    And I go to application previously created
    Then the application is removed from "Enforcement Unit Cases to Review" queue

    Examples:
    | name    | product    | part_number | clc_rating  | end_user_name | end_user_address| country | consignee_name    | consignee_address | end_use                  |
    | Test    | Rifle      | PN-ABC-123  | PL9002      | Joe bloggs    | 123 Main street | BL      | Josephine Bloggs  | 123 Main Street   | Research and development |
