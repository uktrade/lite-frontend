@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @mod_clear_advice
  Scenario: MOD clear advice journey
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
    And I enter "approval reason" as the approval reasons
    And I click add licence condition
    And I click continue
    And I enter "licence condition" into the licence condition
    And I click continue
    And I enter "instruction for exporter" as the instructions for the exporter on the instructions step
    And I enter "reporting footnote" as the reporting footnote on the instructions step
    And I click continue
    Then I see "approval reason" as the reasons for approving
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
    When I click "Clear recommendation"
    And I click confirm
    Then I am asked what my recommendation is
    When I click back
    Then I see there are no recommendations from "MOD-CapProt"
