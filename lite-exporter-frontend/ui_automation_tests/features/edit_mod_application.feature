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
    And I change my reference name
    Then I see my edited reference name
    When I click on goods
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
    When I remove an additional document
    And I confirm I want to delete the document
    And I click the back link
    Then the document is removed from the application

  @LT_1980_edit_MOD_clearance @regression
  Scenario: Edit a F680 Clearance Application
    Given I go to exporter homepage and choose Test Org
    And I create a F680 clearance application via api
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I change my reference name
    Then I see my edited reference name
    When I click on goods
    And I remove a good from the application
    Then the good has been removed from the application
    When I click the back link
    And I remove the end user off the application
    Then no end user is set on the application
    When I click on the application third parties link
    And I remove a third party from the application
    Then the third party has been removed from the application
    When I remove an additional document
    And I confirm I want to delete the document
    And I click the back link
    Then the document is removed from the application

  @LT_1980_edit_MOD_clearance @regression
  Scenario: Edit a Gifting Clearance Application
    Given I go to exporter homepage and choose Test Org
    And I create a gifting clearance application via api
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I change my reference name
    Then I see my edited reference name
    When I click on goods
    And I remove a good from the application
    Then the good has been removed from the application
    When I click the back link
    And I remove the end user off the application
    Then no end user is set on the application
    When I click on the application third parties link
    And I remove a third party from the application
    Then the third party has been removed from the application
    When I remove an additional document
    And I confirm I want to delete the document
    And I click the back link
    Then the document is removed from the application
