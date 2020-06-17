@all @internal
Feature: I want to generate and view compliance cases on approval and proviso of OIEL, OICL and specific SIEL applications

  @regression
  Scenario: Create compliance case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And all flags are removed
    And I create a proviso picklist
    And I create a standard advice picklist
    And the status is set to "submitted"
    And I create a letter paragraph picklist
    When I go to letters
    And I create a letter template for a document
    And I add a letter paragraph to template
    And I preview template
    And I click continue
    And I go to application previously created
    And I click on the user advice tab
    And I select all items in the user advice view
    And I choose to 'approve' the licence
    And I import text from the 'text' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I select that a footnote is not required
    And I click continue
    When I combine all user advice
    And I combine all team advice
    And I finalise the goods and countries
    When I select approve for all combinations of goods and countries
    And I click continue
    And I click continue
    And I generate a decision document
    And I click continue
    Then the status has been changed in the application
    When I go to the compliance case created
    And I click on the licences tab
    And I show filters
    And I search for the finalised licence
    And I apply filters
    Then I see my previously created licence

