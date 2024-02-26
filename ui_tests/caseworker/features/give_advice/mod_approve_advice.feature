@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @mod_approve_advice
  Scenario: MOD approve advice journey
    ##### MOD to circulate a case #####
    Given I sign in to SSO or am signed into SSO
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

    ##### Sub-advisor to give advice #####
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
    And I enter "reason for approving" as the reasons for approving
    And I click the text "Add a licence condition, instruction to exporter or footnote"
    And I enter "licence condition" as the licence condition
    And I enter "instruction for exporter" as the instructions for the exporter
    And I enter "reporting footnote" as the reporting footnote
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
    When I click move case forward
    Then I don't see previously created application

    # FCDO Team deal with it..
    When I switch to "FCDO" with queue "FCDO Cases to Review" and I submit the case
    And I switch to "FCDO" with queue "FCDO Counter-signing" and I submit the case with decision "decision"
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "Review and combine"

    ##### MOD-ECJU to consolidate #####
    When I go to my profile page
    And I change my team to "MOD-ECJU" and default queue to "Review and combine"
    And I go to my case list
    Then I should see my case in the cases list
    When I click the application previously created
    And I assign myself to the case
    And I click the recommendations and decision tab
    And I expand the details for "MOD-ECJU has approved with licence conditions"
    Then I see "reason for approving" as the reasons for approving
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
    When I click "Review and combine"
    And I enter "overall reason" as the overall reason
    And I enter "licence condition1" as the licence condition
    And I click submit recommendation
    Then I see "overall reason" as the overall reason
    And I see "licence condition1" as the licence condition
    When I click move case forward
    Then I don't see previously created application
