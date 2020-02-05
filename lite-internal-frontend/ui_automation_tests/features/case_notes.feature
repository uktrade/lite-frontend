@all @internal @case_notes
Feature: I want to add an internal note to a case and view notes
  As a logged in government user
  I want to add an internal note to a case and view existing notes
  So that I can record my findings and comments and others users can see these

  @LT_911_add @regression
  Scenario: Add a new valid case note
    Given I create open application or open application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I enter "This application is potentially risky." for case note
    And I click post note
    Then note is displayed

  @LT_911_too_many @regression
  Scenario: Add a case note with too many characters
    Given I create open application or open application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I enter "too many characters" for case note
    Then the case note is disabled

  @LT_911_cancel @regression
  Scenario: Case note cancel button
    Given I create open application or open application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I enter "Case note to cancel" for case note
    And I click cancel button
    Then entered text is no longer in case note field

  @LT_912_add_external @smoke
  Scenario: Add a new exporter visible case note
    Given I create open application or open application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I enter "This note is visible to exporters." for case note
    And I click visible to exporters checkbox
    And I click post note
    And I click confirm on confirmation box
    Then note is displayed
