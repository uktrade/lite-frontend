@all @internal @picklists
Feature: I want standard picklists
  As a logged in government user
  I want to define items for one of 6 picklists
  And activate/deactivate items on these picklists
  So that I can make it easier for other government users to quickly apply any relevant conditions to their approval recommendations

  @skip @legacy
  Scenario: Add and edit a letter paragraph
    Given I sign in to SSO or am signed into SSO
    When I go to My Team
    And I go to picklists tab
    And I go to "letter_paragraph" picklist
    And I click add a new picklist
    And I add a new picklist item with "name" and "description"
    And I click continue
    Then I see my new picklist item in the list
    When I click on my picklist item
    Then I see my picklist page with status as "Active"
    When I edit my picklist to "edit" and "edit"
    Then I see my picklist page with status as "Active"

  @skip @legacy
  Scenario: Deactivate and reactivate a picklist item
    Given I sign in to SSO or am signed into SSO
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
