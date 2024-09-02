@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @lu_nlr_advice
  Scenario: LU NLR advice journey
    # Setup
    Given I sign in as Test UAT user
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
