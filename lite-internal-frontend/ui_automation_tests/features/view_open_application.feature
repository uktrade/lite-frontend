@all @open
Feature: View an Open Applications

  @regression @open_application
  Scenario: View an Open Application
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
    When I go to the case
    Then I see the case page
    When I go to the activity tab
    When filter user_type has been changed to "Exporter"
    Then exporter is at the first audit in the trail
    When filter user_type has been changed to "Internal"
    Then exporter is not in the audit trail
