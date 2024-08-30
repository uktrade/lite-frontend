@all @internal @case_notes
Feature: I want to add an internal note to a case and view notes
  As a logged in government user
  I want to add an internal note to a case and view existing notes
  So that I can record my findings and comments and others users can see these

  @add_case_note
  Scenario: Add a new valid case note
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I click on the notes and timeline tab
    And I enter "case note" as the case note
    And I click post note
    Then I see "case note" as a case note


  Scenario: Case note cancel button
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I click on the notes and timeline tab
    And I enter "Case note to cancel" as the case note
    And I click cancel button
    Then entered text is no longer in case note field
