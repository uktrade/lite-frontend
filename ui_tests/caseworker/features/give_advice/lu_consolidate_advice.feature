@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @lu_consolidate_advice
  Scenario: LU consolidate advice journey
    Given I sign in as Licensing Unit Officer
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    When I go to my case list
    And I go to my case list
    And I click the application previously created
    And I assign myself as case officer to the case
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I enter "reason for approving" as the reasons for approving
    And I enter "licence condition" as the licence condition
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "licence condition" as the licence condition
    And I see countersign required warning message
    When I click move case forward
    And I logout
    And I sign in as Licensing Unit Manager
    And I go to my case list
    And I click the application previously created
    And I assign myself as case adviser to the case
    And I click the recommendations and decision tab
    And I click "Review and countersign"
    And I agree with outcome and provide "licensing manager approved" as countersign comments
    And I click submit recommendation
    Then I see "licensing manager approved" as countersign comments
    When I click move case forward
    And I logout
    And I sign in as Licensing Unit Officer
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Finalise case"
    And I click save
    And I click "Generate"
    And I select the template "SIEL template"
    And I click continue
    And I click preview
    Then I see the licence number on the SIEL licence preview
    And I see that "16. Control list no" is "ML1a" on the SIEL licence preview
    When I click continue
    And I click save and publish to exporter
    And I click on "Details" tab
    Then I see the case status is now "Finalised"
    And I see the case is not assigned to any queues

  @lu_consolidate_advice_ogd_licence_conditions
  Scenario: LU consolidate advice with OGD licence conditions
    Given I sign in as Test UAT user
    And I create standard application or standard application has been previously created
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

    ##### MOD Sub-advisor to give advice #####
    When I go to my profile page
    And I change my team to "MOD-CapProt" and default queue to "MOD-CapProt cases to review"
    And I go to my case list
    Then I should see my case in the cases list
    When I click the application previously created
    And I assign myself to the case
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I enter "reason for approving" as the approval reasons
    And I click add licence condition
    And I click continue
    And I enter "MOD licence condition" into the licence condition
    And I click continue
    And I enter "instruction for exporter" as the instructions for the exporter on the instructions step
    And I enter "reporting footnote" as the reporting footnote on the instructions step
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "MOD licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote


    ##### FCDO Sub-advisor to give advice #####
    When I go to my profile page
    And I change my team to "FCDO" and default queue to "FCDO Cases to Review"
    And I go to my case list
    Then I should see my case in the cases list
    When I click the application previously created
    And I assign myself to the case
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I select countries "GB, UA"
    And I enter "reason for approving" as the reasons for approving
    And I click the text "Add a licence condition, instruction to exporter or footnote"
    And I enter "FCDO licence condition" as the licence condition
    And I enter "instruction for exporter" as the instructions for the exporter
    And I enter "reporting footnote" as the reporting footnote
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "FCDO licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote

    When I logout
    Given I sign in as Licensing Unit Officer
    And I prepare the application for final review
    When I go to my case list
    And I go to my case list
    And I click the application previously created
    And I assign myself as case officer to the case
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I enter "reason for approving" as the reasons for approving
    And I click "Add licence condition"
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "MOD licence condition" in the licence condition
    And I see "FCDO licence condition" in the licence condition
    And I see "serial numbers" in the licence condition
