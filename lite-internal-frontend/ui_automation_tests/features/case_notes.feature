@internal @case_notes
Feature: Case notes
  As a...

  Scenario: Add a new valid case note
    Given I go to internal homepage
    When I click on application previously created
    And I enter "text" for case note
    And I click post note
    Then note is displayed

  Scenario: Add a case note filled to max with space characters
    Given I go to internal homepage
    When I click on application previously created
    And I enter "the maximum limit with spaces" for case note
    And I click post note
    Then maximum case error is displayed

  Scenario: Add a case note with too many characters
    Given I go to internal homepage
    When I click on application previously created
    And I enter "the maximum limit" for case note
    Then case note warning is "You have 0 characters remaining"
    When I enter "T" for case note
    Then case note warning is "You have 1 character too many"
    And post note is disabled

  Scenario: Case note cancel button
    Given I go to internal homepage
    When I click on application previously created
    And I enter "Case note to cancel" for case note
    And I click cancel button
    Then entered text is no longer in case note field