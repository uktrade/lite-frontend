@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @fcdo_approve_advice
  Scenario: FCDO to approve advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "FCDO Cases to Review" queue
    And I go to my profile page
    And I change my team to "FCDO" and default queue to "FCDO Cases to Review"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I select countries "GB, UA"
    And I enter "Hello World" as the reasons for approving
    And I click the text "Add a licence condition, instruction to exporter or footnote"
    And I enter "licence condition" as the licence condition
    And I enter "instruction for exporter" as the instructions for the exporter
    And I enter "reporting footnote" as the reporting footnote
    And I click submit recommendation
    Then I should see my recommendation for "Great Britain, Ukraine" with "Hello World"
    When I click move case forward
    Then I don't see previously created application
    # Check the case has moved to the correct queue
    When I go to my profile page
    And I change my team to "FCDO" and default queue to "FCDO Counter-signing"
    And I go to my case list
    Then I should see my case in the cases list
    # Check the recommendation is listed
    When I click the application previously created
    And I click the recommendations and decision tab
    And I expand the details for "FCDO has approved"
    Then I should see my recommendation for "Great Britain, Ukraine" with "Hello World"

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


  @mod_edit_advice
  Scenario: MOD edit advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "MOD-CapProt cases to review" queue
    And I go to my profile page
    And I change my team to "MOD-CapProt" and default queue to "MOD-CapProt cases to review"
    And I go to my case list
    And I click the application previously created
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
    When I click "Edit recommendation"
    And I enter "reason for approving1" as the reasons for approving
    And I click the text "Add a licence condition, instruction to exporter or footnote"
    And I enter "licence condition1" as the licence condition
    And I enter "instruction for exporter1" as the instructions for the exporter
    And I enter "reporting footnote1" as the reporting footnote
    And I click submit recommendation
    Then I see "reason for approving1" as the reasons for approving
    And I see "licence condition1" as the licence condition
    And I see "instruction for exporter1" as the instructions for the exporter
    And I see "reporting footnote1" as the reporting footnote


  @mod_clear_advice
  Scenario: MOD clear advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "MOD-CapProt cases to review" queue
    And I go to my profile page
    And I change my team to "MOD-CapProt" and default queue to "MOD-CapProt cases to review"
    And I go to my case list
    And I click the application previously created
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
    When I click "Clear recommendation"
    And I click confirm
    Then I am asked what my recommendation is
    When I click back
    Then I see there are no recommendations from "MOD-CapProt"


  @mod_refuse_advice
  Scenario: MOD refuse advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "MOD-CapProt cases to review" queue
    And I go to my profile page
    And I change my team to "MOD-CapProt" and default queue to "MOD-CapProt cases to review"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click refuse all
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "reason for this refusal" as the reasons for refusal
    And I click submit recommendation
    Then I see "reason for this refusal" as the reasons for refusal
    # The following step will implicitly navigate through the "All cases" queue
    When I go to application previously created
    And I click the recommendations and decision tab
    And I expand the details for "MOD-CapProt has refused"
    Then I see "reason for this refusal" as the reasons for refusal
    And I see "1a, 1b, 1c, 1d, 1e, 1f" as the refusal criteria


  @lu_consolidate_advice
  Scenario: LU consolidate advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    When I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I assign myself to the case
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
    And I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing manager countersigning"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and countersign"
    And I agree with outcome and provide "licensing manager approved" as countersign comments
    And I click submit recommendation
    Then I see "licensing manager approved" as countersign comments
    When I click move case forward
    And I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
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


  @lu_refuse_advice
  Scenario: LU refuse advice journey
    # Setup
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    # OGD refusal
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "MOD-CapProt cases to review" queue
    And I go to my profile page
    And I change my team to "MOD-CapProt" and default queue to "MOD-CapProt cases to review"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click refuse all
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "reason for this refusal" as the reasons for refusal
    And I click submit recommendation
    And I click move case forward
    When I go to my profile page
    And I change my team to "MOD-ECJU" and default queue to "Review and combine"
    And I go to my case list
    Then I should see my case in the cases list
    When I click the application previously created
    And I assign myself to the case
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I click refuse
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "reason for this refusal" as the reasons for refusal
    And I click submit recommendation
    And I click move case forward
    # Scenario starts
    When I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I click refuse
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "refusal meeting note" as refusal meeting note
    And I click submit recommendation
    Then I see "refusal meeting note" as refusal meeting note
    And I see "1a, 1b, 1c, 1d, 1e, 1f" as the refusal criteria
    When I click the recommendations and decision tab
    And I click "Finalise case"
    And I click save
    And I click "Generate"
    And I select the template "Refusal letter template"
    And I click continue
    And I click preview
    Then I see the application reference on the document preview
    When I click continue
    And I click save and publish to exporter
    And I click on "Details" tab
    Then I see the case status is now "Finalised"
    And I see the case is not assigned to any queues


  @lu_nlr_advice
  Scenario: LU NLR advice journey
    # Setup
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I prepare the application for final review NLR
    # Scenario starts
    When I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I assign myself to the case
    And I go to my case list
    And I click the application previously created
    Then for the first good I see "N/A" for "Control entry"
    And for the first good I see "No" for "Licence required"
    And for the first good I see "Not added" for "Report summary"
    When I click the recommendations and decision tab
    And I click "Review and combine"
    And I enter "reason for approving" as the reasons for approving
    And I enter "licence condition" as the licence condition
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "licence condition" as the licence condition
    And I see countersign required warning message
    When I click move case forward
    And I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing manager countersigning"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and countersign"
    And I agree with outcome and provide "licensing manager approved" as countersign comments
    And I click submit recommendation
    Then I see "licensing manager approved" as countersign comments
    When I click move case forward
    And I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Finalise case"
    And I click save
    Then the document name should be "No Licence Required"
    When I click "Generate"
    And I select the template "No licence required letter template"
    And I click continue
    And I click preview
    Then I see the application reference on the document preview
    And I see the product name under name on the document preview
    When I click continue
    And I click save and publish to exporter
    And I click on "Details" tab
    Then I see the case status is now "Finalised"
    And I see the case is not assigned to any queues

  @lu_countersign
  Scenario: LU countersign
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    When I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I assign myself to the case
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
    And I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing manager countersigning"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and countersign"
    And I agree with outcome and provide "licensing manager approved" as countersign comments
    And I click submit recommendation
    Then I see "licensing manager approved" as countersign comments
    When I click move case forward
    And I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
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

@lu_refuse_advice_inform_letter
  Scenario: LU inform letter
    # Setup
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    # OGD refusal
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "MOD-CapProt cases to review" queue
    And I go to my profile page
    And I change my team to "MOD-CapProt" and default queue to "MOD-CapProt cases to review"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click refuse all
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "reason for this refusal" as the reasons for refusal
    And I click submit recommendation
    And I click move case forward
    When I go to my profile page
    And I change my team to "MOD-ECJU" and default queue to "Review and combine"
    And I go to my case list
    Then I should see my case in the cases list
    When I click the application previously created
    And I assign myself to the case
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I click refuse
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "reason for this refusal" as the reasons for refusal
    And I click submit recommendation
    And I click move case forward
    # Scenario starts
    When I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I click refuse
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "refusal meeting note" as refusal meeting note
    And I click submit recommendation
    Then I see "Inform letter" in decision documents
    When I click "Create Inform letter" button
    And I select "Weapons of mass destruction (WMD)" radio button
    And I click continue
    And I click preview
    And I click continue
    # Sending Inform letter
    Then I see "READY TO SEND" inform letter status in decision documents
    When I click "Send inform letter" button
    And I click the application previously created
    And I click the recommendations and decision tab
    Then I see "SENT" inform letter status in decision documents
    # Edit Inform letter
    When I click inform letter edit link
    And I edit template with "something"
    And I click preview
    Then I see the "something" text on the document preview
    # It goes to Generate decision document screen after continue
    When I click continue
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    # Re-create Inform letter
    When I click "Recreate" button
    And I select "Military" radio button
    And I click continue
    And I click preview
    Then I see the "under the Military End-Use Control of Article 4(2) of retained Council Regulation (EC) No 428/2009" text on the document preview
    When I click continue
    Then I see "READY TO SEND" inform letter status in decision documents
