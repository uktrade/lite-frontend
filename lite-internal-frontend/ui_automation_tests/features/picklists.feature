@all @internal @picklists
Feature: I want standard picklists
  As a logged in government user
  I want to define items for one of 6 picklists
  And activate/deactivate items on these picklists
  So that I can make it easier for other government users to quickly apply any relevant conditions to their approval recommendations

  @LT_1077_add_edit @smoke
  Scenario: Add and edit a picklist item with context variables
    Given I go to internal homepage
    When I go to My Team
    And I go to picklists tab
    And I go to "letter_paragraph" picklist
    And I click add a new picklist
    And I add a new picklist item with "name" and "description {{ fake_variable }}"
    And I click continue
    Then An invalid variable error for "fake_variable" is shown
    When I clear the picklist name and description
    And I add a new picklist item with "name" and "description"
    And I type {{ into the description
    Then I am given context variable suggestions
    When I click a suggested context variable
    And I click continue
    Then I see my new picklist item in the list
    When I click on my picklist item
    Then I see my picklist page with status as "Active"
    When I edit my picklist to "edit" and "edit"
    Then I see my picklist page with status as "Active"

  @LT_1077_deactivate @regression
  Scenario: Deactivate and reactivate a picklist item
    Given I go to internal homepage
    When I go to My Team
    And I go to picklists tab
    And I go to "report_summary" picklist
    And I click add a new picklist
    And I add a new picklist item with "name" and "description"
    And I click continue
    And I click on my picklist item
    And I deactivate my picklist
    Then I see my picklist page with status as "Deactivated"
    When I reactivate my picklist
    Then I see my picklist page with status as "Active"
