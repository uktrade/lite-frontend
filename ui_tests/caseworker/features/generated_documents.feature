@internal @documents @generated_documents @all
Feature: I want to select a template to generate a document to the applicant on a case
As a logged in government user
I want to select a template to generate a document to the applicant on a case
So that I can easily and quickly generate different types of standard document to send to the applicant

  @skip @legacy
  Scenario: Generate a document for a case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And I create a template
    When I go to application previously created
    And I click on the Generate document button
    And I select the template previously created
    And I leave the default addressee
    Then I see the template text to edit
    When I add my custom text "yellowDuck"
    Then I see the template text to edit
    When I click continue
    Then I see the generated document preview
    When I click continue
    Then I see my generated document
    # Test Regenerate
    When I click regenerate
    Then I see the template text to edit
    When I click continue
    Then I see the generated document preview
    When I click continue
    Then I see both my generated documents

  @skip @legacy
  Scenario: Generate a document with an addressee for a case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And I create a template
    And I create an additional contact for the case
    When I go to application previously created
    And I click on the Generate document button
    And I select the template previously created
    And I select the addressee previously created
    Then I see the template text to edit
    When I click continue
    Then I see the generated document preview
    And I see the addressee in the document
    When I click continue
    Then I see my generated document
