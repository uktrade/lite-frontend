@all @internal @organisation
Feature: I want to add a company to LITE
  As a logged in government user
  I want to add a new company to LITE
  So that the new company can make applications


  Scenario: Review and approve an organisation
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
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

  Scenario: Review and reject an organisation
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And an anonymous user applies for an organisation
    When I navigate to organisations
    And I click on In review tab
    Then I should see details of organisation previously created
    When I click on the organisation and click Review
    Then I should see a summary and option to approve or reject organisation
    When I reject the organisation
    Then the organisation should be set to "Rejected"
    And the "rejected" organisation appears in the audit trail

  @check_company_details
  Scenario: Check company details
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And an anonymous user creates and organisation for review with <eori_number>,<uk_vat_number>,<primary_site>,<phone_number>,<registration_number>
    When I navigate to organisations
    And I click on In review tab
    Then I should see details of organisation previously created
    When I click on the organisation and click Review
    Then I should see a summary along with registered office address
    When I select approve and Save
    Then the organisation should be set to "Active"
    And the "activated" organisation appears in the audit trail
    When I navigate to organisations
    And I click on Active tab
    Then I should see details of organisation previously created

    Examples:
    |eori_number    | uk_vat_number | primary_site             | phone_number  | registration_number |
    |GB205672212000 | 123456789     | HQ London United Kingdom | +441234567890 | GB111111            |
