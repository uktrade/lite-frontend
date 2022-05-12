@all @internal @sanctions
Feature: I want to check sanctions matches
  As a logged in government user
  I want to check that the sanction match is highlighted
  For a case is created with a name on it that has a sanction

  Scenario: check a sanction match is highlighted
    Given I sign in to SSO or am signed into SSO
    And I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    When I go to application previously created
    Then I should see that the sanction match is highlighted as <end_user_name>

    Examples:
    | name    | product         | part_number | clc_rating  | end_user_name | end_user_address                                                               | country | consignee_name | consignee_address                               | end_use                  |
    | Test    | Rifle1, Rifle2  | PN-ABC-123  | PL9002      | ABDUL AZIZ    | Sheykhan Village, Pirkowti Area, Orgun District, Paktika Province, Afghanistan | BE      | ABDUL AHAD     | Shega District, Kandahar Province, Afghanistan  | Research and development |
