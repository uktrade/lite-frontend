@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @mod_edit_advice
  Scenario: MOD edit advice journey
    Given I sign in as Test UAT user
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
