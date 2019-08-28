@case_notes @all
Feature: I want to add a note to an application and view notes
  As a logged in exporter
  I want to add a note to an application and view existing notes
  So that I can record my findings and comments and others users can see these

  @LT_1119_add
  Scenario: Add a new valid case note
    Given I go to exporter homepage and choose Test Org
    And an application exists
    When I click on applications
    And I click on application previously created
    And I enter "This is a note on my application!" for case note
    And I click post note
    Then note is displayed

  @LT_1119_max
  Scenario: Add a case note filled to max with space characters
    Given I go to exporter homepage and choose Test Org
    And an application exists
    When I click on applications
    And I click on application previously created
    And I enter "the maximum limit with spaces" for case note
    And I click post note
    Then maximum case error is displayed

  @LT_1119_too_many
  Scenario: Add a case note with too many characters
    Given I go to exporter homepage and choose Test Org
    And an application exists
    When I click on applications
    And I click on application previously created
    And I enter "the maximum limit" for case note
    Then case note warning is "You have 0 characters remaining"
    When I enter "the maximum limit plus 1" for case note
    Then case note warning is "You have 1 character too many"
    And post note is disabled

  @LT_1119_cancel
  Scenario: Case note cancel button
    Given I go to exporter homepage and choose Test Org
    And an application exists
    When I click on applications
    And I click on application previously created
    And I enter "Case note to cancel" for case note
    And I click cancel button
    Then entered text is no longer in case note field