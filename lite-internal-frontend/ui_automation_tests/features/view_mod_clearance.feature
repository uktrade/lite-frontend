@all @MOD
Feature: View an MOD Clearance

  @smoke @exhibition_view
  Scenario: View an Exhibition Clearance
    Given I sign in to SSO or am signed into SSO
    And an Exhibition Clearance is created
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
    When I go to the case
    Then I see the case page

  @regression @F680_view
  Scenario: View an F680 Clearance
    Given I sign in to SSO or am signed into SSO
    And a F680 Clearance is created
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
    When I go to the case
    Then I see the case page

  @regression @gifting_view
  Scenario: View an Gifting Clearance
    Given I sign in to SSO or am signed into SSO
    And  a Gifting Clearance is created
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
    When I go to the case
    Then I see the case page
