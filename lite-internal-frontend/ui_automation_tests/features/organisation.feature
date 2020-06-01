@all @internal @organisation
Feature: I want to add a company to LITE
  As a logged in government user
  I want to add a new company to LITE
  So that the new company can make applications

  @LT_934_register_commercial_organisation @regression
  Scenario: Registering a commercial organisation
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new commercial organisation
    Then commercial organisation is registered
    When I click the organisation
    And I edit the organisation
    Then organisation is edited
    And the "updated" organisation appears in the audit trail

  @LT_1417_register_individual_organisation @regression
  Scenario: Registering an individual
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new individual organisation
    Then individual organisation is registered
    When I click the organisation
    Then the "created" organisation appears in the audit trail

  @LT_1008_register_hmrc_organisation @regression
  Scenario: Registering an HMRC organisation
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new HMRC organisation
    And I go to organisations
    Then HMRC organisation is registered
    When I click the organisation
    Then the "created" organisation appears in the audit trail

  @LT_1086_adding_a_flag_to_an_organisation @regression
  Scenario: Adding a flag to an organisation
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I add a flag at level Organisation
    And I go to application previously created
    And I go to the organisation which submitted the case
    And I click the edit flags link
    And I select previously created flag
    Then the "added" flag appears in the audit trail
    And the previously created organisations flag is assigned
    When I go to open application previously created
    Then the previously created organisations flag is assigned to the case
    When I go to the internal homepage
    Then I see previously created application
    And I see the added flags on the queue

  @LT_1105_review_and_approve_an_organisation @regression
  Scenario: Review and approve an organisation
    Given I sign in to SSO or am signed into SSO
    And an anonymous user applies for an organisation
    When I go to organisations
    And I go to the in review tab
    Then the organisation previously created is in the list
    When I click the organisation
    And I click review
    Then I should see a summary of organisation details
    When I approve the organisation
    Then the organisation should be set to "Active"
    And the "activated" organisation appears in the audit trail
    When I go to organisations
    And I go to the active tab
    Then the organisation previously created is in the list
    # Check user gets a warning if a matching organisation exists
    When an organisation matching the existing organisation is created
    And I go to the organisation
    And I click review
    Then I should be warned that this organisation matches an existing one

  @LT_1105_review_and_reject_an_organisation @regression
  Scenario: Review and reject an organisation
    Given I sign in to SSO or am signed into SSO
    And an anonymous user applies for an organisation
    When I go to organisations
    And I go to the in review tab
    Then the organisation previously created is in the list
    When I click the organisation
    And I click review
    Then I should see a summary of organisation details
    When I reject the organisation
    Then the organisation should be set to "Rejected"
    And the "rejected" organisation appears in the audit trail
