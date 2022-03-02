@all @internal @approve_case
Feature: I want to approve a case for a newly created application
  As a logged in government user working on a specific case that is assigned to me
  I want to approve the case and verify that it has moved queues.

  @approve_case
  Scenario: Approve a case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign the case to "FCO Cases to Review" queue
    And I go to my profile page
    And I change my team to "FCO" and default queue to "FCO Cases to Review"
    When I go to my case list
    And I click the application previously created
    And I click on the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I select countries "GB, UA"
    And I enter "Hello World" as the reasons for approving
    And I submit the recommendation
    Then I should see my recommendation for "Great Britain, Ukraine" with "Hello World"
    When I click move case forward
    Then I dont see previously created application

    When I go to my profile page
    And I change my team to "FCO" and default queue to "FCO Counter-signing"
    And I go to my case list
    Then I should see my case in the cases list

    When I click the application previously created
    And I click on the recommendations and decision tab
    And I expand the details for "FCO has approved"
    Then I should see my recommendation for "Great Britain, Ukraine" with "Hello World"
