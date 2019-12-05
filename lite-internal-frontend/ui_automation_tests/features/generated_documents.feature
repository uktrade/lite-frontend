@internal @documents @generated_documents
Feature: I want to select a template to generate a document to the applicant on a case
As a logged in government user
I want to select a template to generate a document to the applicant on a case
So that I can easily and quickly generate different types of standard document to send to the applicant

  @LT_1028_generate_document
  Scenario: Generate a document for a case
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    And I create a template
    When I go to application previously created
    And I click on the Generate document button
#  Commenting out the test as no pagination on index LT-1828
#    And I select the template previously created
#    Then I see the generated document preview
#    When I click continue
#    Then I see my generated document
