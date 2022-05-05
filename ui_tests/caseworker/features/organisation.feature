@all @internal @organisation
Feature: I want to add a company to LITE
  As a logged in government user
  I want to add a new company to LITE
  So that the new company can make applications

  @skip @legacy
  Scenario: Registering a commercial organisation
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new commercial organisation
    Then commercial organisation is registered
    When I click the organisation
    And I edit the organisation
    Then organisation is edited
    And the "updated" organisation appears in the audit trail

  @skip @legacy
  Scenario: Registering an individual
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new individual organisation
    Then individual organisation is registered
    When I click the organisation
    Then the "created" organisation appears in the audit trail

  @skip @legacy
  Scenario: Registering an HMRC organisation
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new HMRC organisation
    And I go to organisations
    Then HMRC organisation is registered
    When I click the organisation
    Then the "created" organisation appears in the audit trail

  Scenario: Review and approve an organisation
    Given I sign in to SSO or am signed into SSO
    And an anonymous user applies for an organisation
    When I navigate to organisations
    And I click on In review tab
    Then I should see details of organisation previously created
    When I click on the organisation and click Review
    Then I should see a summary and option to approve or reject organisation
    When I select approve and Save
    Then the organisation should be set to "Active"
    And the "activated" organisation appears in the audit trail
    When I navigate to organisations
    And I click on Active tab
    Then I should see details of organisation previously created

  @skip @legacy
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

  @check_company_details
  Scenario: Check company details
    Given I sign in to SSO or am signed into SSO
    And an anonymous user creates and organisation for review with <eori_number>,<uk_vat_number>,<primary_site>,<phone_number>
    When I navigate to organisations
    And I click on In review tab
    Then I should see details of organisation previously created
    When I click on the organisation and click Review
    Then I should see a summary along with primary site
    When I select approve and Save
    Then the organisation should be set to "Active"
    And the "activated" organisation appears in the audit trail
    When I navigate to organisations
    And I click on Active tab
    Then I should see details of organisation previously created

    Examples:
    |eori_number    | uk_vat_number | primary_site              | phone_number   |
    |GB205672212000 | 123456789     | HQ London United Kingdom  | +448922296634  |
