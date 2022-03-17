@licence @edit @all @standard
Feature: I want to be able to edit and update an active application
  As a logged in exporter
  I want to be able to edit and update an active application
  So that any additional information and/or corrected details can be updated on my application

  @skip @legacy
  Scenario: Edit a trade control application
    Given I go to exporter homepage and choose Test Org
    And I create a trade control application via api
    # Ensure automation doesn't move application to non-editable state
    And the status is set to "submitted"
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I click on the "reference-name" section
    And I enter a licence name
    Then I see my edited reference name
    When I click on the "location" section
    And I remove a location from the application
    Then the location has been removed from the application
    When I click the back link
    And I click on the "goods" section
    And I remove a good from the application
    Then the good has been removed from the application
    When I click the back link
    And I click on the "end_user" section
    And I remove the end user off the application
    Then no end user is set on the application
    When I click on the "consignee" section
    And I remove the consignee off the application
    Then no consignee is set on the application
    When I click on the "third-parties" section
    And I remove a third party from the application
    Then the third party has been removed from the application
    When I click on the "supporting-documents" section
    And I remove an additional document
    And I confirm I want to delete the document
    And I click the back link
    Then the document has been removed from the application
