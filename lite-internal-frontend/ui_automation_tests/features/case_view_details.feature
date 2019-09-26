@internal @view_cases
Feature: I want to view the case details of a case
  As a Logged in government user
  I want to view the details on a case
  So that I can make review the case before making any decisions

@LT_1042_can_see_all_parties
  Scenario: Gov user can see all parties on the case
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    Then I see an end user
    And I see an ultimate end user
    And I see a third party
    And I see a consignee
