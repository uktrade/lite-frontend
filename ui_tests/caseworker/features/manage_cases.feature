@all @internal @manage_cases @setup
Feature: I want to record the final decision overall on an application case
  As a Licensing Unit Case Officer
  I want to record the final decision overall on an application case
  So that this can be communicated back to the party that raised the case
  As a: logged in government user
  I want to: update the status of an application case
  So that: interested users can see the progress of the application case and whether it is complete

  @skip @legacy
  Scenario: Change status to Under Review
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click change status
    And I select status "Under review" and save
    Then the status has been changed in the application
