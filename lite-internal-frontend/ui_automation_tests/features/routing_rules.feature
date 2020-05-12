@all @internal @routing_rules
Feature: I want to have cases be automatically routed to relevant work queues and users based on
  case sub-type, country and combinations of flags on the case
  So that I can focus on working the case and not on routing cases to the correct departments

  @LT_1063_create @regression
  Scenario: Create routing rule
    Given I sign in to SSO or am signed into SSO
    And a new queue has been created
    When I add a flag at level Case
    And I go to routing rules list
    And I add a routing rule of tier "5", a status of "Submitted", my queue, and all additional rules for my team
    Then I see the routing rule in the rule list


  @LT_1063_deactivate_activate_edit @regression
  Scenario: Deactivate, Activate, Edit a routing rule
    Given I sign in to SSO or am signed into SSO
    And a new queue has been created
    When I add a flag at level Case
    And I go to routing rules list
    And I add a routing rule of tier "5", a status of "Submitted", my queue, and all additional rules for my team
    Then I see the routing rule in the rule list
    When I edit my routing rule with tier "10", a status of "Finalised", and no additional rules
    Then I see the routing rule in the list as "Active" and tier "10"
    When I deactivate my routing rule
    Then I see the routing rule in the list as "Deactivated" and tier "10"

  @LT_2109_routing_rules_automation @regression
   Scenario: Routing rule automation
    Given I sign in to SSO or am signed into SSO
    And an Exhibition Clearance is created
    And a new queue has been created
    When I go to routing rules list
    And I add a routing rule of tier "1", a status of "Submitted", my queue, and no additional rules for my team
    And I go to application previously created
    And I click change status
    And I select status "Submitted" and save
    And I click to rerun routing rules, and confirm
    Then I see my queue in assigned queues
    When I go to routing rules list
    And I deactivate my routing rule
    Then I see the routing rule in the list as "Deactivated" and tier "1"
