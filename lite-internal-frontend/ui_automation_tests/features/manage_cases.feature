@internal @manage_cases @setup
Feature: I want to record the final decision overall on an application case
  As a Licensing Unit Case Officer
  I want to record the final decision overall on an application case
  So that this can be communicated back to the party that raised the case
  As a: logged in government user
  I want to: update the status of an application case
  So that: interested users can see the progress of the application case and whether it is complete

  @LT_909_status
  Scenario: Change status to Under Review
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click progress application
    And I select status "Under review" and save
    Then the status has been changed in the application
    And the application headers and information are correct

  @LT_957_record
  Scenario: Record decision
    Given I create application or application has been previously created
    And I go to internal homepage
    When I give myself the required permissions for "Make final decisions"
    And I go to application previously created
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
    And I reset the permissions

  @LT_957_optional
  Scenario: Record decision without optional text
    Given I create application or application has been previously created
    And I go to internal homepage
    When I give myself the required permissions for "Make final decisions"
    And I go to application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I select decision "2b"
    And I click continue
    Then I see application "denied"
    And I reset the permissions

  @LT_957_multiple
  Scenario: Record decision with multiple decision
    Given I create application or application has been previously created
    And I go to internal homepage
    When I give myself the required permissions for "Make final decisions"
    And I go to application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I select decision "1a"
    And I select decision "2b"
    And I select decision "6c"
    And I click continue
    Then I see application "denied"
    And I reset the permissions

  @LT_957_error
  Scenario: Record decision validation
    Given I create application or application has been previously created
    And I go to internal homepage
    When I give myself the required permissions for "Make final decisions"
    And I go to application previously created
    And I click record decision
    And I "deny" application
    And I click continue
    And I click continue
    Then I see error message "Select at least one denial reason"
    And I reset the permissions


  @LT_1042_can_see_ultimate_end_users
  Scenario: Gov user can see ultimate end users in the destinations section of the case
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    Then I see an ultimate end user

  @LT-956_can_see_advice_view
  Scenario: Gov user can see advice view page
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click on view advice
