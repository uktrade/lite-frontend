@licence @submit @all @standard
Feature: I want to create MOD Licence Applications
  As a logged in exporter
  I want to apply for an MOD clearance for equipment or information if I need one
  So that I can get approval to provide the relevant equipment or information to a third party outside the UK

  @LT_1169_exhibition_clearance @setup @smoke
  Scenario: Submit Exhibition Clearance Application
    Given I go to exporter homepage and choose Test Org
    When I select a licence of type "mod"
    And I select a MOD licence of type "exhibition_clearance"
    And I enter a licence name
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    When I click on goods
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on end user
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I click on consignees
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then wait for download link
    When I click the back link
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application
