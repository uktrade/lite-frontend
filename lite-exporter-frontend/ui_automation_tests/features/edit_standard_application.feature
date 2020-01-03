@licence @edit @all @standard
Feature: I want to be able to edit and update an active application
  As a logged in exporter
  I want to be able to edit and update an active application
  So that any additional information and/or corrected details can be updated on my application

  @LT_998_edit_standard_application_slow @regression
  Scenario: Edit a standard application
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I change my reference name
    Then I see my edited reference name
    When I change my reference number
    Then I see my edited reference number
    When I click on standard goods tile
    And I remove a good from the application
    Then the good has been removed from the application
    When I click the back link
    And I remove the end user off the application
    Then no end user is set on the application
    When I remove the consignee off the application
    Then no consignee is set on the application
    When I click on the application third parties link
    And I remove a third party from the application
    Then the third party has been removed from the application
    When I click the back link
    And I remove an additional document
    And I confirm I want to delete the document
    Then the document is removed from the application

  @LT_998_edit_standard_application_fast @regression
  Scenario: Edit a standard application with audit
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I change my reference name
    And I submit the application
    And I go to application previously created
    And I click on activity tab
    Then "updated the status to: submitted" is shown as position "1" in the audit trail
    And "updated the application name" is shown as position "2" in the audit trail
