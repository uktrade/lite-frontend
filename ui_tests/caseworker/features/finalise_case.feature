@all @internal @finalise
Feature: I want to finalise a case
  As a logged in gov user
  I want to be prompted to generate the right documents for the appropriate decision
  So that this can be communicated back to the exporter and they can download and view their licence or clearance

  @skip @legacy
  Scenario: Finalise and approve a case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And all flags are removed
    And the status is set to "submitted"
    And I "approve" all elements of the application at user and team level
    And A template exists for the appropriate decision
    When I go to the team advice page by url
    And I combine all team advice
    And I go to the final advice page by url
    And I finalise the advice
    Then I see the applied for goods details on the licence page
    When I click continue
    Then I see the final advice documents page
    And The decision row status is "not-started"
    When I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    Then The decision row status is "done"
    When I click continue
    And I go to application previously created
    Then The licence information is in the second audit
    When I go to the documents tab
    Then The generated decision document is visible
    # reissue
    When I go to application previously created
    And I click change status
    And I select status "Re-opened for changes" and save
    When I go to the final advice page by url
    And I finalise the advice
    Then I see the applied for goods details on the licence page
    When I click continue
    Then I see the final advice documents page
    And The decision row status is "not-started"
    When I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    Then The decision row status is "done"
    When I click continue
    And I go to application previously created
    Then The licence information is in the second audit
    When I go to the documents tab
    Then The generated decision document is visible

  @skip @legacy
  Scenario: Finalise and refuse a case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And all flags are removed
    And the status is set to "submitted"
    And I "refuse" all elements of the application at user and team level
    And A template exists for the appropriate decision
    When I go to the team advice page by url
    And I combine all team advice
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
    And I go to application previously created
    Then The case is finalised and a document is created in the audits
    When I go to the documents tab
    Then The generated decision document is visible

  @skip @legacy
  Scenario: Finalise and approve an open application case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And all flags are removed
    And the status is set to "submitted"
    And I "approve" the open application good and country at all advice levels
    And A template exists for the appropriate decision
    When I go to the final advice page by url
    And I finalise the advice
    Then I see the good country combination
    When I approve the good country combination
    And I click continue on the approve open licence page
    Then I see the final advice documents page
    And The decision row status is "not-started"
    When I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    Then The decision row status is "done"
    When I click continue
    And I go to application previously created
    Then The licence information is in the second audit
    When I go to the documents tab
    Then The generated decision document is visible

  @skip @legacy
  Scenario: Finalise and refuse an open application case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And all flags are removed
    And the status is set to "submitted"
    And I "refuse" the open application good and country at all advice levels
    And A template exists for the appropriate decision
    When I go to the final advice page by url
    And I finalise the advice
    Then I see the refused good country combination
    When I click continue
    And I click continue
    Then I see the final advice documents page
    And The decision row status is "not-started"
    When I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    Then The decision row status is "done"
    When I click continue
    And I go to application previously created
    Then The case is finalised and a document is created in the audits
    When I go to the documents tab
    Then The generated decision document is visible
