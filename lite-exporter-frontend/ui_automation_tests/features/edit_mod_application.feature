@licence @edit @all @MOD
Feature: I want to be able to edit MOD Licence Applications
  As a logged in exporter
  I want to apply for an MOD clearance for equipment or information if I need one
  So that I can get approval to provide the relevant equipment or information to a third party outside the UK

  @LT_1169_edit_exhibition_clearance @regression
  Scenario: Edit a Exhibition Clearance Application
    Given I go to exporter homepage and choose Test Org
    And I create a exhibition clearance application via api
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I click on the "reference-name" section
    And I enter a licence name
    Then I see my edited reference name
    When I click on the "exhibition-details" section
    And I enter Exhibition details with the name "123"
    Then The "exhibition-details" section is set to status "done"
    When I click on the "goods" section
    And I remove a good from the application
    Then the good has been removed from the application
    When I click the back link
    And I click on the "supporting-documents" section
    And I remove an additional document
    And I confirm I want to delete the document
    And I click the back link
    Then the document has been removed from the application

  @LT_1598 @LT_1980_edit_f680_clearance @regression
  Scenario: Edit an F680 Clearance Application
    Given I go to exporter homepage and choose Test Org
    And I create a F680 clearance application via api
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I click on the "reference-name" section
    And I enter a licence name
    Then I see my edited reference name
    When I click on the "clearance" section
    And I choose a clearance level for my application
    When I click on the "goods" section
    And I remove a good from the application
    Then the good has been removed from the application
    When I click the back link
    When I click on the "end_user" section
    And I remove the end user off the application
    Then no end user is set on the application
    When I click on the "third-parties" section
    And I remove a third party from the application
    Then the third party has been removed from the application
    When I click on the "supporting-documents" section
    When I remove an additional document
    And I confirm I want to delete the document
    And I click the back link
    Then the document has been removed from the application

  @LT_1980_edit_gifting_clearance @regression
  Scenario: Edit a Gifting Clearance Application
    Given I go to exporter homepage and choose Test Org
    And I create a gifting clearance application via api
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I click on the "reference-name" section
    And I enter a licence name
    Then I see my edited reference name
    When I click on the "goods" section
    And I remove a good from the application
    Then the good has been removed from the application
    When I click the back link
    And I click on the "end_user" section
    And I remove the end user off the application
    Then no end user is set on the application
    When I click on the "third-parties" section
    And I remove a third party from the application
    Then the third party has been removed from the application
    When I click on the "supporting-documents" section
    When I remove an additional document
    And I confirm I want to delete the document
    And I click the back link
    Then the document has been removed from the application
