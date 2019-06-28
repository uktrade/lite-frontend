@internal @manage_cases @setup
Feature: I want to record the final decision overall on an application case
  As a Licensing Unit Case Officer
  I want to record the final decision overall on an application case
  So that this can be communicated back to the party that raised the case
  As a: logged in government user
  I want to: update the status of an application case
  So that: interested users can see the progress of the application case and whether it is complete

  @LT-909_status
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

  @LT-957_record
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

  @LT-957_optional
  Scenario: Record decision without optional text
    Given I go to internal homepage
    When I click on application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I select decision "2b"
    And I click continue
    Then I see application "denied"

  @LT-957_multiple
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

  @LT-957_error
  Scenario: Record decision validation
    Given I go to internal homepage
    When I click on application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I click continue
    Then I see error message "Select at least one denial reason"
