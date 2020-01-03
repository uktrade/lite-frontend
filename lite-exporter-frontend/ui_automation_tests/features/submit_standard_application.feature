@licence @submit @all @standard
Feature: I want to indicate the standard licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1091_draft @regression
  Scenario: Apply for a licence to draft and delete
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    Then I see the application overview
    When I delete the application

  @LT_1091_standard @setup @smoke
  Scenario: Submit standard application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I add a non incorporated good to application
    Then good is added to application
    When I click on end user
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I click the back link
    Then Wait for "end_user_document_download" to be present
    When I click on consignees
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I click the back link
    Then Wait for "consignee_document_download" to be present
    And I see end user on overview
    When I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1091_external @regression
  Scenario: Submit standard application with external locations and ultimate end users
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click on ultimate end users
    And I click on the add button
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    When I upload a file "file_for_doc_upload_test_1.txt"
    Then Wait for download link
    And "Delete" link is present
    When I click on the add button
    And I add an end user of sub_type: "commercial", name: "Mr Jones", website: " ", address: "London" and country "Ukraine"And I upload a file "file_for_doc_upload_test_1.txt"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I remove an ultimate end user so there is one less and return to the overview
    Then there is only one ultimate end user
    When I click on application locations link
    And I select "external" for where my goods are located
    And I select "new" for whether or not I want a new or existing location to be added
    And I fill in new external location form with name: "32 Lime Street", address: "London" and country: "Ukraine" and continue
    And I click on add new address
    And I fill in new external location form with name: "place", address: "1 Paris Road" and country: "Ukraine" and continue
    Then I see "2" locations
    When I click on preexisting locations
    And I select the location at position "2" in external locations list and continue
    And I click the back link
    When I click on end user
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I click the back link
    Then Wait for "end_user_document_download" to be present
    When I click on consignees
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I click the back link
    Then Wait for "consignee_document_download" to be present
    When I submit the application
    And I click applications
    Then I see submitted application
