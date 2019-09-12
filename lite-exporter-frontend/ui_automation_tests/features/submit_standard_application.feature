@licence @submit @all @standard
Feature: I want to indicate the standard licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1091_draft
  Scenario: Apply for a licence to draft and delete
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    Then I see the application overview
    When I delete the application

  @LT_1091_standard @setup
  Scenario: Submit standard application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I add a non incorporated good to application
    Then good is added to application
    When I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I wait for the end user document to be processed
    Then I see end user on overview
    When I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1091_external
  Scenario: Submit standard application with external locations
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click on application locations link
    And I select "external" for where my goods are located
    And I click on add new address
    And I fill in new external location form with name: "32 Lime Street", address: "London" and country: "Ukraine" and continue
    And I click on add new address
    And I fill in new external location form with name: "place", address: "1 Paris Road" and country: "Ukraine" and continue
    Then I see "2" locations
    When I click on preexisting locations
    And I select the location at position "2" in external locations list and continue
    And I click on application overview
    And I add a non incorporated good to application
    Then good is added to application
    When I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I wait for the end user document to be processed
    And I submit the application
    And I click applications
    Then I see submitted application

  @LT_1042_happy_path
  Scenario: Apply for a licence with ultimate end users
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click on ultimate end users
    And I click on ultimate end users add button
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I click on ultimate end users add button
    And I add an end user of type: "commercial", name: "Mr Jones", website: " ", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I remove an ultimate end user so there is one less and return to the overview
    Then there is only one ultimate end user
    When I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I wait for the end user document to be processed
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1445_ultimate_end_user_upload_download_delete
  Scenario: Add an Ultimate end user document and can download and delete
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click on ultimate end users
    And I click on ultimate end users add button
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I click back link
    Then "Attach" link is present
    When I click on attach a document
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then Wait for download link
    And "Delete" link is present
    When I delete the ultimate end user document
    Then "Attach" link is present
