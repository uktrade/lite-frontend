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
        And I add a good or good type with description "123 pistol" controlled "Yes" control code "1234" incorporated "No" and part number "321"
        Then I see good in goods list
        When I edit a good to description "edited" controlled "Yes" control code "1234" incorporated "No" and part number "321"
        Then I see my edited good in the goods list
        When I delete my good
        Then my good is no longer in the goods list

    @LT_1006_add_clc_query_good
    Scenario: Add "I don't know" good
        Given I go to exporter homepage and choose Test Org
        When I click on goods link
        And I click add a good button
        And I add a good or good type with description "Hand pistol" controlled "Unsure" control code " " incorporated "No" and part number "321"
        And I upload file "file_for_doc_upload_test_1.txt" with description "Doesnt matter really"
        And I raise a clc query control code "ML17" description "Unsure what this is"
        Then I see the clc query in goods list

    @LT_1142_add_a_document
    Scenario: Add a document
        Given I go to exporter homepage and choose Test Org
        When I click on goods link
        And I add a good and attach a document
        Then I see the document has been attached
