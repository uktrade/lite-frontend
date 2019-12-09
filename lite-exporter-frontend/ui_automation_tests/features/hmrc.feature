@HMRC @all
Feature: I want to be able to perform actions as a HMRC user

  @LT_1008_log_in_as_hmrc_and_select_organisation_to_raise_query_for @smoke
  Scenario: Raise an HMRC Query
    # This has the second org in the seed data as a hmrc org, this is to save on multiple accesses to great sso
    Given I have a second set up organisation
    And I go to exporter homepage and choose Test Org
    When I switch organisations to my second organisation
    And I select to raise a query for my first organisation
    And I click continue
    And I click on hmrc set end user
    And I add an end user of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I wait for document to upload
    And I click the back link
    And I click on hmrc describe your goods
    When I add a good or good type with description "M4" controlled "Yes" control code "ML1a" incorporated "No" and part number "not needed"
    And I click the back link
    And I click on application hmrc locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I click on hmrc explain your reasoning
    And I leave a note for the "reasoning"
    And I click continue
    When I submit the application
    Then application is submitted
