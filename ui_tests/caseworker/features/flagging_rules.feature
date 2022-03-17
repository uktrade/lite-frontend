@all @internal @flagging_rules
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @skip @legacy
  Scenario: Create flagging rules
    Given I sign in to SSO or am signed into SSO
    And I create all types of flag except organisation
    When I go to flagging rules list
    And I add a flagging rule of type "Case", with condition "oiel", and flag
    And I add a goods flagging rule with condition "ML1a", flag and answer "True" for only apply to verified goods
    And I add a flagging rule of type "Destination", with condition "China", and flag
    Then I see the flagging rules in the flag list as "Active"
    When I deactivate all my new flagging rules
    And I show filters
    And I click include deactivated
    Then I see the flagging rules in the flag list as "Deactivated"
