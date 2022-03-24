@all @internal @case_notes
Feature: I want to add an internal note to a case and view notes
  As a logged in government user
  I want to add an internal note to a case and view existing notes
  So that I can record my findings and comments and others users can see these

  @add_case_note
  Scenario: Add a new valid case note
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I click on the notes and timeline tab
    And I enter "case note" as the case note
    And I click make visible to exporter
    And I click post note
    And I click confirm on confirmation box
    Then I see "case note" as a case note

  @skip @legacy
  Scenario: Add a case note with too many characters
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click on the case notes tab
    And I enter "too many characters" for case note
    Then the case note is disabled

  @skip @legacy
  Scenario: Case note cancel button
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click on the case notes tab
    And I enter "Case note to cancel" for case note
    And I click cancel button
    Then entered text is no longer in case note field

  @skip @legacy
  Scenario: Add a new exporter visible case note
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to application previously created
    And I click on the case notes tab
    And I enter "This note is visible to exporters." for case note
    And I click visible to exporters checkbox
    And I click post note
    And I click confirm on confirmation box
    Then note is displayed
