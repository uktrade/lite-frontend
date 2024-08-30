@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @fcdo_approve_advice
  Scenario: FCDO to approve advice journey
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
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
