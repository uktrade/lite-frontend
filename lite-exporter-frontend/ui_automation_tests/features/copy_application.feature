@copy_application @all
Feature: I want to add a note to an application and view notes
  As a logged in exporter
  I want to add a note to an application and view existing notes
  So that I can record my findings and comments and others users can see these

  @LT_972_copy_standard @smoke
  Scenario: Add a copy a standard application
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    When I go to application previously created
    And I click copy application
    And I add a name "copied application", and select "yes" to being referred with code "1234-54"
    Then I see my new name added
    And I see the new reference code added
    And the application contains products
    And the application contains end users
    And the application contains consignees
    And I see no supporting documents on the application
