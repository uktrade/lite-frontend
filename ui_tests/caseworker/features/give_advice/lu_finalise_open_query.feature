@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @skip
  Scenario: LU cannot finalise a case if there is an open query
    Given I sign in as Licensing Unit Officer
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    When I go to my case list
    And I click the application previously created
    And I assign myself as case officer to the case
    And I click the queries tab
    And I click "Send a query to the exporter"
    And I enter "Provide data sheet for line item1" as the query
    And I click send
    Then I see "Provide data sheet for line item1" as the query under open queries
    When I click the recommendations and decision tab
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
    And I click the application previously created under open queries tab
    And I assign myself as case adviser to the case
    And I click the recommendations and decision tab
    And I click "Review and countersign"
    And I agree with outcome and provide "licensing manager approved" as countersign comments
    And I click submit recommendation
    Then I see "licensing manager approved" as countersign comments
    When I click move case forward
    And I logout
    And I sign in as Licensing Unit Officer
    And I click the application previously created under open queries tab
    And I click the recommendations and decision tab
    Then I see warning that case cannot be finalised due to a query that needs to be closed
