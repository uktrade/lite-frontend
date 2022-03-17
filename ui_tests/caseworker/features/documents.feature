@all @internal @documents @document_upload
Feature: I want to attach related documents to a case and view attached documents
As a logged in government user
I want to attach related documents to a case and view attached documents
So that it is recorded against the case and available for other case workers to view

  @skip @legacy
  Scenario: Upload a new document that doesn't contain a virus
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I go to the documents tab
    And I click on the Attach Document button
    And I upload file "file_for_doc_upload_test_1.txt" with description "Doesnt matter really"
    And I click on the Attach Document button
    And I upload file "file_for_doc_upload_test_2.txt" with description "Still doesnt matter"
    Then file "file_for_doc_upload_test_2.txt" with description "Still doesnt matter" is on position "0"
    And file "file_for_doc_upload_test_1.txt" with description "Doesnt matter really" is on position "1"

  @skip @legacy
  Scenario: Download the good and end user document of a submitted application
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    Then I can click on the good document download link
    And I can click on the end user document download link
    And I can click on the additional document download link
