@internal @templates
Feature: I want to configure standard templates for letter generation
As a logged in government user
I want to configure standard templates for letter generation
So that I can create standard letters used by case workers and they can be updated when required


  @LT_1029_add_template
  Scenario: Add template
    Given I sign in to SSO or am signed into SSO
    And I go to internal homepage
    And I create a letter paragraph picklist
    When I go to letters
    And I create a letter template for ECJU letter
    And I add a letter paragraph to template
    Then I see the drag and drop page
    When I preview template
    Then my picklist is in template
    When I click save
    Then I see my template in the table


  @LT_1029_add_template
  Scenario: Add Licence template
    Given I sign in to SSO or am signed into SSO
    And I go to internal homepage
    And I create a letter paragraph picklist
    When I go to letters
    And I create a letter template for document
    And I add a letter paragraph to template
    Then I see the drag and drop page
    When I preview template
    Then my picklist is in template
    When I click save
    Then I see my template in the table

  @LT_1029_view_and_edit_template
  Scenario: View and edit a created template
    Given I create a document template
    And I sign in to SSO or am signed into SSO
    And I go to internal homepage
    When I go to letters
    And I click on my template
    Then The template details are present
    And The paragraph text is present
    When I edit my template name and layout
    Then The template details are present
    When I edit my template paragraphs
    Then The template paragraphs have been edited
    When I click save
    Then The paragraph text is present

