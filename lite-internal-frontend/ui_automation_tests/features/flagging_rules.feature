#@all @internal @flagging_rules
#Feature: I want to add case-level flags to a case and view them
#  As a logged in government user
#  I want to toggle one or more flags on and off a case to highlight key features
#  So that all users viewing the case can quickly and easily see the aspects which might require more attention
#
#  @LT_985_create @regression
#  Scenario: Create flagging rules
#    Given I sign in to SSO or am signed into SSO
#    When I add a flag at level Case
#    And I go to flagging rules list
#    And I add a flagging rule of type "Case", with condition "oiel", and flag
#    Then I see the flagging rule in the flag list
#    When I add a flag at level Good
#    And I go to flagging rules list
#    And I add a flagging rule of type "Good", with condition "Ml1a", and flag
#    Then I see the flagging rule in the flag list
#    When I add a flag at level Destination
#    And I go to flagging rules list
#    And I add a flagging rule of type "Destination", with condition "China", and flag
#    Then I see the flagging rule in the flag list
#
#
#  @LT_985_deactivate_activate_edit @regression
#  Scenario: Deactivate, Activate, Edit a flagging rule
#    Given I sign in to SSO or am signed into SSO
#    When I go to flagging rules list
#    And I add a flag at level Case
#    And I add a flagging rule of type "Case", with condition "oiel", and flag
#    When I edit my "Case" flagging rule with condition "siel"
#    Then I see the flagging rule in the list as "Active"
#    When I deactivate my flagging rule
#    And I show filters
#    And I click include deactivated
#    Then I see the flagging rule in the list as "Deactivated"
