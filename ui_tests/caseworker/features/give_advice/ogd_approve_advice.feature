@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @ogd_approve_advice
  Scenario: DESNZ to approve advice journey
    Given I sign in as Test UAT user
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "DESNZ Chemical cases to review" queue
    And I go to my profile page
    And I change my team to "DESNZ Chemical" and default queue to "DESNZ Chemical cases to review"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I enter "Hello World" as the approval reasons
    And I click add licence condition
    And I click continue
    And I enter "licence condition" into the licence condition
    And I click continue
    And I enter "instruction for exporter" as the instructions for the exporter on the instructions step
    And I enter "reporting footnote" as the reporting footnote on the instructions step
    And I click continue
    Then I see "Hello World" as the reasons for approving
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
    When I click move case forward
    Then I don't see previously created application
