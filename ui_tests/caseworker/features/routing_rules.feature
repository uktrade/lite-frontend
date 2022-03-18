@all @internal @routing_rules
Feature: I want to have cases be automatically routed to relevant work queues and users based on
  case sub-type, country and combinations of flags on the case
  So that I can focus on working the case and not on routing cases to the correct departments

  @skip @legacy
  Scenario: Create routing rule
    Given I sign in to SSO or am signed into SSO
    And a queue has been created
    When I add a flag at level Case
    And I go to routing rules list
    And I add a routing rule of tier "5", a status of "Submitted", my queue, and all additional rules for my team
    And I filter by my routing rule queue
    Then I see the routing rule in the rule list
    When I edit my routing rule with tier "10", a status of "Finalised", and no additional rules
    And I filter by my routing rule queue
    Then I see the routing rule in the list as "Active" and tier "10"
    When I deactivate my routing rule
    And I filter by my routing rule queue
    Then I see the routing rule in the list as "Deactivated" and tier "10"

  @skip @legacy
   Scenario: Routing rule automation
    Given I sign in to SSO or am signed into SSO
    And an Exhibition Clearance is created
    And a queue has been created
    When I go to routing rules list
    And I add a routing rule of tier "1", a status of "Submitted", my queue, and no additional rules for my team
    And I go to application previously created
    And I click change status
    And I select status "Submitted" and save
    And I click to rerun routing rules, and confirm
    Then I see my queue in assigned queues
    When I go to routing rules list
    And I filter by my routing rule queue
    And I deactivate my routing rule
    And I filter by my routing rule queue
    Then I see the routing rule in the list as "Deactivated" and tier "1"

    Scenario: Move case along in workflow
      Given I sign in to SSO or am signed into SSO
      And I create standard application or standard application has been previously created
      When I go to my profile page
      And I change my team to "Licensing Reception" and default queue to "Open cases"
      And I go to my case list
      And I switch to queue "Licensing Reception SIEL applications"
      Then I see previously created application
      When I click on the application previously created
      Then I should see the button "I'm done"
      When I click I'm done
      And I click submit
      Then the case should have been removed from my default queue
      When I go to my profile page
      And I change my team to "Enforcement Unit" and default queue to "Enforcement Unit Cases to Review"
      And I go to my case list
      Then I should see my case in the cases list
      When I go to my profile page
      And I change my team to "Technical Assessment Unit" and default queue to "Technical Assessment Unit SIELs to Review"
      And I go to my case list
      Then I should see my case in the cases list
