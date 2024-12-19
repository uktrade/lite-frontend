@case_notes @all
Feature: I want to add a note to an application and view notes
  As a logged in exporter
  I want to add a note to an application and view existing notes
  So that I can record my findings and comments and others users can see these

  Scenario: view a case note added by caseworker
    Given I signin and go to exporter homepage and choose Test Org
    And I submit an application with <name>,<product>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>,<is_mod_security_approved>
    And caseworker inputs a case note as "case note"
    When I go to exporter homepage
    Then I see a notification next to check progress
    When I click check progress
    Then I see a notification next to the application
    When I click on my application
    Then I see a notification next to Notes
    When I click the notes tab
    Then I see "case note" as the case notes

    Examples:
    | name    | product | clc_rating  | end_user_name      | end_user_address  | country | consignee_name      | consignee_address   | end_use                  | is_mod_security_approved |
    | Test    | Rifle   | PL9002      | Automated End user | 1234, High street | BE      | Automated Consignee | 1234, Trade centre  | Research and development | False                    |
