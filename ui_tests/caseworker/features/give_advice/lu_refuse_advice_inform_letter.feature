@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

@lu_refuse_advice_inform_letter
  Scenario: LU inform letter
    # Setup
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
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
