@internal @case_notes
Feature: I want to add an internal note to a case and view notes
  As a logged in government user
  I want to add an internal note to a case and view existing notes
  So that I can record my findings and comments and others users can see these

  @LT-911_add
  Scenario: Add a new valid case note
    Given I create application or application has been previously created
    And I go to internal homepage
    When I click on application previously created
    And I enter "This application is potentially risky." for case note
    And I click post note
    Then note is displayed

  @LT-911_max
  Scenario: Add a case note filled to max with space characters
    Given I create application or application has been previously created
    And I go to internal homepage
    When I click on application previously created
    And I enter "the maximum limit with spaces" for case note
    And I click post note
    Then maximum case error is displayed

  @LT-911_too_many
  Scenario: Add a case note with too many characters
    Given I create application or application has been previously created
    And I go to internal homepage
    When I click on application previously created
    And I enter "the maximum limit" for case note
    Then case note warning is "None"
    When I enter "T" for case note
    Then case note warning is "disabled"
    And post note is disabled

  @LT-911_cancel
  Scenario: Case note cancel button
    Given I create application or application has been previously created
    And I go to internal homepage
    When I click on application previously created
    And I enter "Case note to cancel" for case note
    And I click cancel button
    Then entered text is no longer in case note field

  @LT-912_add_external
  Scenario: Add a new exporter visible case note
    Given I create application or application has been previously created
    And I go to internal homepage
    When I click on application previously created
    And I enter "This note is visible to exporters." for case note
    And I click visible to exporters checkbox
    And I click post note
    And I click confirm on confirmation box
    Then note is displayed

  @LT-912_add_external_to_clc_query
  Scenario: Add a new exporter visible case note to clc query
    Given I create clc query or clc query has been previously created
    And I go to internal homepage
    When I click on the clc-case previously created
    And I enter "This clc query note is visible to exporters." for case note
    And I click visible to exporters checkbox
    And I click post note
    And I click confirm on confirmation box
