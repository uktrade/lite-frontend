@ecju_queries @all
Feature: As a logged in exporter
I want to see when there are ECJU queries (RFIs) relating to my applications, queries and licences and be able to respond
So that I can quickly identify where action is required by me and respond to any queries

  @LT_996_application @regression
  Scenario: view and respond to a ecju query in an application
    Given I go to exporter homepage and choose Test Org
    When I go to the recently created application with ecju query
    And I click the ECJU Queries tab
    And I click to respond to the ecju query
    And I enter "This is my response" for ecju query and click submit
    And I select "no" for submitting response and click submit
    And I enter "This is my edited response" for ecju query and click submit
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed

  @LT_996_clc @regression
   Scenario: view and respond to a ecju query in a good
    Given I go to exporter homepage and choose Test Org
    When I click on an CLC query previously created
    And I click the ECJU Queries tab
    And I click to respond to the ecju query
    And I enter "This is my response" for ecju query and click submit
    And I select "no" for submitting response and click submit
    And I enter "This is my edited response" for ecju query and click submit
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed

  @LTD_305_ecju_query_response_without_document @regression
  Scenario: view an ecju query, provide response without uploading documents
    Given I go to exporter homepage and choose Test Org
    When I go to the recently created application with ecju query
    And I click the ECJU Queries tab
    And I click to respond to the ecju query
    And I enter my response as "Uploading requested documents"
    And I click "add_document"
    And I select that I cannot attach a document
    And I see ECJU helpline details
    And I select a valid missing document reason
    And I see the missing document reason text "No document attached: Document is above OFFICIAL-SENSITIVE"
    And I click "submit"
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed

  @LTD_305_ecju_query_response_with_document @regression
  Scenario: view an ecju query, provide response and upload documents
    Given I go to exporter homepage and choose Test Org
    When I go to the recently created application with ecju query
    And I click the ECJU Queries tab
    And I click to respond to the ecju query
    And I enter my response as "Uploading requested documents"
    And I click "add_document"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "Supporting document for the query"
    And I see "1" documents ready to be included in the response
    And I click "add_document"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "Supporting document for the query"
    And I see "2" documents ready to be included in the response
    And I click "submit"
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed

  @LTD_305_ecju_query_response_upload_and_delete_document @regression
  Scenario: view an ecju query, provide response and upload and delete document
    Given I go to exporter homepage and choose Test Org
    When I go to the recently created application with ecju query
    And I click the ECJU Queries tab
    And I click to respond to the ecju query
    And I enter my response as "Uploading requested documents"
    And I click "add_document"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "Supporting document for the query"
    And I see "1" documents ready to be included in the response
    And I delete document "1" from the response
    And I see the missing document reason text "There are no documents."
    And I click "submit"
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed
