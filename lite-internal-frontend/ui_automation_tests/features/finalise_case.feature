@all @internal @finalise
Feature: I want to finalise a case
  As a logged in gov user
  I want to be prompted to generate the right documents for the appropriate decision
  So that this can be communicated back to the exporter and they can download and view their licence or clearance

  @LT_2035_generate_documents_and_licence @regression
  Scenario: Finalise and approve a case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I "approve" all elements of the application at user and team level
    And A template exists for the appropriate decision
    When I go to the final advice page by url
    And I combine all advice
    And I finalise the advice
    And I click continue on the licence page
    Then I see the final advice documents page
    And The decision row status is "not-started"
    When I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    Then The decision row status is "done"
    When I click continue
    Then The licence information is in the latest audit
    When I click on the Documents button
    Then The generated decision document is visible

  @LT_2035_generate_documents_and_licence @regression
  Scenario: Finalise and refuse a case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I "refuse" all elements of the application at user and team level
    And A template exists for the appropriate decision
    When I go to the final advice page by url
    And I combine all advice
    And I finalise the advice
    And I click continue
    Then I see the final advice documents page
    And The decision row status is "not-started"
    When I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    Then The decision row status is "done"
    When I click continue
    Then The case is finalised and a document is created in the audits
    When I click on the Documents button
    Then The generated decision document is visible