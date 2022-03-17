@all @internal @templates
Feature: I want to configure standard templates for letter generation
As a logged in government user
I want to configure standard templates for letter generation
So that I can create standard letters used by case workers and they can be updated when required

  @skip @legacy
  Scenario: Create a Template
    Given I sign in to SSO or am signed into SSO
    And I create a letter paragraph picklist
    When I go to letters
    And I create a letter template for a document
    And I add a letter paragraph to template
    Then I see the drag and drop page
    When I preview template
    Then my picklist is in template
    When I click continue
    Then I see my template in the table

  @skip @legacy
  Scenario: View and edit a created template
    Given I sign in to SSO or am signed into SSO
    And I create a document template
    And I create a letter paragraph picklist
    When I go to letters
    And I click on my template
    Then The template details are present
    And The paragraph text is present
    When I edit my template name and layout
    Then The template details are present
    And "updated letter template types from oiel, siel to f680, oiel, siel" is shown as position "1" in the audit trail
    And "updated letter template name from" is shown as position "2" in the audit trail
    And "to" is shown as position "2" in the audit trail
    When I edit my template paragraphs
    Then The template paragraphs have been edited
    When I click done
    Then The paragraph text is present
    And "updated letter paragraphs from" is shown as position "1" in the audit trail
