@licence @edit @all @standard
Feature: I want to be able to edit and update an active application
  As a logged in exporter
  I want to be able to edit and update an active application
  So that any additional information and/or corrected details can be updated on my application

  @LT_998_edit_standard_application @regression
  Scenario: Edit a standard application
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    When I click on applications
    And I click on application previously created
    And I click edit application
    And I choose to make major edits
    And I change my reference name
    Then I see my edited reference name
    When I change my reference number
    Then I see my edited reference number
    When I click on standard goods tile
    And I remove a good from the application
    Then the good has been removed from the application
    When I click back to the application overview
    And I remove the end user off the application
    Then no end user is set on the application
    When I remove the consignee off the application
    Then no consignee is set on the application
    When I click on the application third parties link
    And I remove a third party from the application
    Then the third party has been removed from the application
    When I click back to the application overview
    And I remove an additional document
    And I confirm I want to delete the document
    Then the document is removed from the application

  @LT_1099_prohibit_edit_application @regression
  Scenario: Cannot edit a read only application
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    When I click on applications
    And my application has been withdrawn
    And I click on application previously created
    Then the edit application button is not present
