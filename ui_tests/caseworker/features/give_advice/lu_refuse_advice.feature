@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @lu_refuse_advice
  Scenario: LU refuse advice journey
    # Setup
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
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
