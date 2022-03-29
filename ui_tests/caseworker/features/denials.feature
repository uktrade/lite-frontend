@all @internal @denials
Feature: I want to check denial matches
  As a logged in government user
  I want to example download denial data in CSV format and update it
  So that I can upload it and check end-user denial matches

  Scenario: Check end-user denial matches against uploaded CSV data
    # Denial upload
    Given I sign in to SSO or am signed into SSO
    And I cleanup any temporary files created
    When I go to the add denial records page
    And I download an example .csv file
    And I update the .csv file with <name>,<address>,<notifying_govmt>,<final_dest>,<item_list_codes>,<item_desc>,<consignee_name>,<end_use>
    And I upload the .csv file
    And I click continue
    Then I should see a banner that says "Denials created successfully"
    # Case creation
    Given I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    When I go to application previously created
    And I select end user "Joe Bloggs"
    And I click "View related denials"
    Then I should see "Joe Bloggs" listed
    When I select "Joe Bloggs"
    And I click "Add as partial match"
    Then I should see "Joe Bloggs" as a partial match
    When I select "Joe Bloggs" under denial matches
    And I click "Remove denial match"
    Then I should not see "Joe Bloggs" as a partial match
    When I select end user "Joe Bloggs"
    And I click "View related denials"
    Then I should see "Joe Bloggs" listed
    When I select "Joe Bloggs"
    And I click "Add as exact match"
    Then I should see "Joe Bloggs" as an exact match
    When I select "Joe Bloggs" under denial matches
    And I click "Remove denial match"
    Then I should not see "Joe Bloggs" as an exact match

    Examples:
    | name        | product  | part_number | clc_rating | end_user_name | end_user_address | country | consignee_name | consignee_address | address          | notifying_govmt  | final_dest | item_list_codes  | item_desc | end_use   |
    | Joe Bloggs  | Rifle1   | PN-ABC-123  | PL9002     | Joe Bloggs    | 123 Main Street  | GE      | John Smith     | 123 Main Street   | 123 Main Street  | France           | Germany    | 1234             | gun       | Test use  |
