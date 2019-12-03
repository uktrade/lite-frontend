@all @internal @review_goods
Feature: I want to review, amend where required and confirm the goods ratings and descriptions on an application
  As a logged in government user
  I want to review, amend where required and confirm the goods ratings and descriptions on a standard application
  So that I can confirm the goods are correctly described


  @LT_1300 @smoke
  Scenario: Review goods
    Given I sign in to SSO or am signed into SSO
    And I create application or application has been previously created
    And I create report summary picklist
    When I go to application previously created
    And I select goods and click review
    And I click on add report summary
    And I respond "yes", "ML4b1", "1", "Because the good is controlled" and click continue
    Then the control list is present on goods review page
