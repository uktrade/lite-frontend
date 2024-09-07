@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @lu_countersign
  Scenario: LU countersign
    Given I sign in as Licensing Unit Officer
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    When I go to my case list
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
