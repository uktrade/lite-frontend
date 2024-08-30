@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @mod_refuse_advice
  Scenario: MOD refuse advice journey
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
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
    And I logout
