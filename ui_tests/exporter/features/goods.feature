@goods @all
Feature: I want to edit and remove goods on the goods list
  As a logged in exporter
  I want to add edit and remove goods on my goods list
  So that I can ensure the correct goods are listed on my goods list

  @skip @legacy
  Scenario: Add, edit and delete good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "one" for a good
    And I add a good with description "123 pistol" part number "321" controlled "True" control code "ML1a" and graded "yes"
    And I add the goods grading with prefix "abc" grading "nato_restricted" suffix "def" issuing authority "NATO" reference "12345" Date of issue "10-05-2015"
    And I specify the "category 1" good details military use "yes_modified" component "yes_general" and information security "Yes"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I get the goods ID
    Then I see good in goods list
    When I edit the good to description "edited" part number "321" controlled "True" and control list entry "ML1a"
    And I edit the "category 1" good details to military use "yes_designed" component "yes_designed" information security "No"
    Then I see my edited good details in the good page
    And I delete document "1" from the good
    When I delete my good
    Then my good is no longer in the goods list

  @skip @legacy
  Scenario: Add queried good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "one" for a good
    And I add a good with description "Hand pistol" part number "321" controlled "None" control code " " and graded "grading_required"
    And I specify the "category 1" good details military use "yes_designed" component "yes_modified" and information security "No"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I raise a clc query control code "ML1a" clc description "I believe it is ML1a" and pv grading reason "I believe the good requires grading"
    Then I see good information
    And I see the good is in a query

  @skip @legacy
  Scenario: Add a new good without a document for a valid reason
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "one" for a good
    And I add a good with description "Hand pistol" part number "321" controlled "None" control code " " and graded "no"
    And I specify the "category 1" good details military use "no" component "no" and information security "No"
    And I select that I cannot attach a document
    Then I see ECJU helpline details
    When I select a valid missing document reason
    When I click the back link
    Then My good is created

  @skip @legacy
  Scenario: Add, edit and delete software good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product category "three-software" for a good
    And I add a good with description "123 software" part number "321" controlled "True" control code "ML1a" and graded "yes"
    And I add the goods grading with prefix "abc" grading "nato_restricted" suffix "def" issuing authority "NATO" reference "12345" Date of issue "10-05-2015"
    And I specify software and technology purpose details for a good that is in those categories
    And I specify the "category 3" good details military use "yes_modified" component "yes_general" and information security "Yes"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I get the goods ID
    Then I see good in goods list
    When I edit the good to description "edited" part number "321" controlled "True" and control list entry "ML1a"
    And I edit the "category 3" good details to military use "yes_designed" component "yes_designed" information security "No"
    And I edit the software and technology purpose details for a good to "edited software purpose"
    Then I see my edited good details in the good page
    When I delete my good
    Then my good is no longer in the goods list

  @skip @legacy
  Scenario: Add and delete firearm good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product type "firearm"
    And I add a good with description "9mm barrel" part number "321" controlled "True" control code "ML1a" and graded "yes"
    And I add the goods grading with prefix "abc" grading "uk_official" suffix "def" issuing authority "MoD" reference "12345" Date of issue "10-05-2015"
    And I enter calibre as "0.45"
    And I specify firearms act sections apply as "Yes"
    And I specify firearms identification markings as "Yes" with details "laser engraving"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I get the goods ID
    Then I see good in goods list
    When I edit the good to description "edited" part number "321" controlled "True" and control list entry "ML1a"
    When I delete my good
    Then my good is no longer in the goods list

  @skip @legacy
  Scenario: Add, edit and delete firearm good
    Given I go to exporter homepage and choose Test Org
    When I click on goods link
    And I click add a good button
    And I select product type "firearm"
    And I add a good with description "9mm barrel" part number "321" controlled "True" control code "ML1a" and graded "yes"
    And I add the goods grading with prefix "abc" grading "uk_official" suffix "def" issuing authority "MoD" reference "12345" Date of issue "10-05-2015"
    And I enter calibre as "0.45"
    And I specify firearms act sections apply as "Yes"
    And I specify firearms identification markings as "Yes" with details "laser engraving"
    And I confirm I can upload a document
    And I upload file "file_for_doc_upload_test_1.txt" with description "This is a file I want to upload to show."
    And I get the goods ID
    Then I see good in goods list
    When I edit the good to description "edited" part number "321" controlled "True" and control list entry "ML1a"
    And I edit the firearm good details to type "components_for_firearm" firearms act applicable "Yes" and identification markings "Yes"
    Then I see my edited good details in the good page
    When I delete my good
    Then my good is no longer in the goods list
