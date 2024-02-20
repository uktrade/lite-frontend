@all @internal @documents @document_upload
Feature: I want to attach related documents to a case and view attached documents
As a logged in government user
I want to attach related documents to a case and view attached documents
So that it is recorded against the case and available for other case workers to view

  Scenario: Upload a new document that doesn't contain a virus
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I go to the documents tab
    And I click on the Attach Document button
    And I upload file "Assessment_summary.txt" with description "Case assessment summary"
    Then I see file "Assessment_summary.txt" with description "Case assessment summary" is uploaded
    When I click on the Attach Document button
    And I upload file "additional_information.txt" with description "Additional information"
    Then I see file "additional_information.txt" with description "Additional information" is uploaded

  @download
  Scenario: Download the good and end user document of a submitted application
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    Then I can click on the consignee document download link
    And I can click on the end user document download link
