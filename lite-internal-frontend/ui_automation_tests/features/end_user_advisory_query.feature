@internal @eua_query
Feature: I want to respond to an End User Advisory query
  As a logged in government user
  I want to respond to an End User Advisory query
  So that I can inform an exporter whether or not an entity is a suitable end user for a potential export licence

  @LT_1474_respond
  Scenario: I want to check that the functionality of other cases exists
    Given I create eua query or eua query has been previously created
    And I sign in to SSO or am signed into SSO
    And I go to internal homepage
    When I go to end user advisory previously created
    Then I should see flags can be added
    And I should see the ability to add case notes
    And The dropdown should contain Move Case, Documents, and Ecju queries

  @LT_1474_change_case_status
  Scenario: I want to check that the case status can be changed
    Given I create eua query or eua query has been previously created
    And I sign in to SSO or am signed into SSO
    And I go to internal homepage
    When I go to end user advisory previously created
    And I click progress application
    And I select status "Closed" and save
    Then the status has been changed in the end user advisory
