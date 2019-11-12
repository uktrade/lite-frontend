@goods @all
Feature: I want to edit and remove goods on the goods list
  As a logged in exporter
  I want to add edit and remove goods on my goods list
  So that I can ensure the correct goods are listed on my goods list

  @LT_928_edit
  Scenario: Edit and delete good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I add a good or good type with description "123 pistol" controlled "Yes" control code "ML1a" incorporated "No" and part number "321"
    Then I see good in goods list
    When I edit a good to description "edited" controlled "Yes" control code "ML1a" incorporated "No" and part number "321"
    Then I see my edited good details in the good page
    When I delete my good
    Then my good is no longer in the goods list

  @LT_1006_add_clc_query_good
  Scenario: Add "I don't know" good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I add a good or good type with description "Hand pistol" controlled "Unsure" control code " " incorporated "No" and part number "321"
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I raise a clc query control code "ML1a" description "I believe it is ML1a"
    Then I see the clc query in goods list

  @LT_1142_add_a_document
  Scenario: Add a document
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I add a good and attach a document
    Then I see the document has been attached

  @LT_886_add_new_good_to_app
  Scenario: Add a new good directly to a standard application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application
    And I click to manage goods on a standard application
    Then I see there are no goods on the application
    When I click Add a new good
    And I add a new good with description "New good for application" controlled "Yes" control code "ML8a25b" incorporated "No" and part number "P123"
    And I enter details for the new good on an application with value "99.98", quantity "13" and unit of measurement "Kilogram(s)" and I click Continue"
    And I attach a document to the good with description "Test good spec 01"
    Then A new good has been added to the application
