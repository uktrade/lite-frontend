Feature: Manage cases
  As a..

  Scenario: Change status to Under Review
    Given I go to internal homepage
    When I click on application previously created
    And I click progress application
    And I select status "Under review" and save
    Then the status has been changed in the application
    And the application headers and information are correct
    #TODO remove dependency here
    When I go to exporter homepage
    And I login to exporter homepage with username "trinity@unicorns.com" and "12345678900"
    And I click applications
    Then the status has been changed in exporter

  Scenario: Record decision
    Given I go to internal homepage
    When I click on application previously created
    And I click record decision
    And I "grant" application
    And I click continue
    Then I see application "granted"
    When I click record decision
    And I click continue
    Then I see application "granted"
    When I click record decision
    And I "deny" application
    And I click continue
    And I select decision "2b"
    And I type optional text "Reason denied due to bad information"
    And I click continue
    Then I see application "denied"
    When I click record decision
    And I click continue
    And I select decision "2b"
    And I click continue
    Then I see application "denied"

  Scenario: Record decision without optional text
    Given I go to internal homepage
    When I click on application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I select decision "2b"
    And I click continue
    Then I see application "denied"

  Scenario: Record decision with multiple decision
    Given I go to internal homepage
    When I click on application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I select decision "1a"
    And I select decision "2b"
    And I select decision "6c"
    And I click continue
    Then I see application "denied"

    Scenario: Record decision validation
    Given I go to internal homepage
    When I click on application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I click continue
    Then I see error message "Select at least one denial reason"
