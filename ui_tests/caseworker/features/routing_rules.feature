@all @internal @routing_rules
Feature: I want to have cases be automatically routed to relevant work queues and users based on
  case sub-type, country and combinations of flags on the case
  So that I can focus on working the case and not on routing cases to the correct departments


  @e2e_routing
  Scenario: End to end routing rules
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And I create standard application or standard application has been previously created
    And I set the case status to "Submitted"
    # LR
    When I switch to "Licensing Reception" with queue "Licensing Reception SIEL applications" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Enforcement Unit Cases to Review, Technical Assessment Unit SIELs to Review"
    # EU
    When I switch to "Enforcement Unit" with queue "Enforcement Unit Cases to Review" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Technical Assessment Unit SIELs to Review"
    And I see the case is not assigned to queues "Enforcement Unit Cases to Review"
    # TAU
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Technical Assessment Unit SIELs to Review"
    And I go to my case list
    Then I see previously created application
    When I click on the application previously created
    And I assign myself to the case
    Then I click on Product assessment
    And I select good
    And I select the CLE "ML1a"
    And I select "components for" / "microwave components" as report summary prefix / subject and regime to none and submit
    When I click move case forward
    Then I don't see previously created application
    # LU
    When I switch to "Licensing Unit" with queue "Licensing Unit Pre-circulation Cases to Review" and I submit the case
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "MOD-DI Indirect cases to review, MOD-CapProt cases to review, FCDO Cases to Review"
    # MOD-DI
    When I switch to "MOD-DI" with queue "MOD-DI Indirect cases to review" and I submit the case
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "MOD-CapProt cases to review, FCDO Cases to Review"
    # MOD-CapProt
    When I switch to "MOD-CapProt" with queue "MOD-CapProt cases to review" and I submit the case
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "FCDO Cases to Review"
    # FCDO
    When I switch to "FCDO" with queue "FCDO Cases to Review" and I submit the case
    And I switch to "FCDO" with queue "FCDO Counter-signing" and I submit the case with decision "decision"
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "Review and combine"
    When I switch to "MOD-ECJU" with queue "Review and combine" and I submit the case with decision "decision"
    Then I see the case status is now "Under final review"
    And I see the case is assigned to queues "Licensing Unit Post-circulation Cases to Finalise"
    When I click on the notes and timeline tab
    Then I see "decision" as a case note


  Scenario: Move case along in workflow
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And I create standard application or standard application has been previously created
    When I go to my profile page
    And I change my team to "Licensing Reception" and default queue to "Open cases"
    And I go to my case list
    And I switch to queue "Licensing Reception SIEL applications"
    Then I see previously created application
    When I click on the application previously created
    And I assign myself to the case
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
