@all @internal @sanctions
Feature: I want to check sanctions matches
  As a logged in government user
  I want to check that the sanction match is highlighted
  For a case is created with a name on it that has a sanction

  Scenario: check a sanction match is highlighted
    Given I sign in as Test UAT user
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    When I go to application previously created
    Then I see the section of the case page entitled Sanction matches
    And I see <end_user_name> listed there
    When I select <end_user_name> and press remove sanction match
    Then I am asked to provide a reason
    And the sanction is removed from the case page

    Examples:
    | name    | product         | part_number | clc_rating  | end_user_name | end_user_address                                                               | country | consignee_name | consignee_address                               | end_use                  |
    | Test    | Rifle1, Rifle2  | PN-ABC-123  | PL9002      | ABDUL AZIZ    | Sheykhan Village, Pirkowti Area, Orgun District, Paktika Province, Afghanistan | BE      | ABDUL AHAD     | Shega District, Kandahar Province, Afghanistan  | Research and development |
