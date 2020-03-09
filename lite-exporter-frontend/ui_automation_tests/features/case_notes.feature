@case_notes @all
Feature: I want to add a note to an application and view notes
  As a logged in exporter
  I want to add a note to an application and view existing notes
  So that I can record my findings and comments and others users can see these

  @LT_1119_add_cancel @smoke
  Scenario: Add a new valid case note
    Given I go to exporter homepage and choose Test Org
    And I create a standard application via api
    When I go to application previously created
    And I click the notes tab
    And I enter text for case note
    And I click cancel button
    Then entered text is no longer in case note field
    When I enter text for case note
    And I click post note
    Then note is displayed
