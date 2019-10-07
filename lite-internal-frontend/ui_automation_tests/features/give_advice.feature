@internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @LT_1376_grant
  Scenario: Give advice and grant a licence
    Given I create application or application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click on view advice
    And I select all items in the advice view
    And I choose to 'approve' the licence
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    Then I see my advice has been posted successfully
    And I see added advice in the same amount of places

  @LT_1376_proviso
  Scenario: Give advice and add a proviso
    Given I create application or application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click on view advice
    And I select all items in the advice view
    And I choose to 'proviso' the licence
    And I import text from the 'proviso' picklist
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    Then I see my advice has been posted successfully
    And I see added advice in the same amount of places

  @LT_1376_deny
  Scenario: Give advice and deny a licence
    Given I create application or application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click on view advice
    And I select all items in the advice view
    And I choose to 'refuse' the licence
    And I select decision "1a"
    And I select decision "2b"
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    Then I see my advice has been posted successfully
    And I see added advice in the same amount of places

  @LT_1378_pre_populate
  Scenario: See that advice pre-populates
    Given I create application or application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click on view advice
    And I select all items in the advice view
    And I choose to 'proviso' the licence
    And I import text from the 'proviso' picklist
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    And I select all items in the advice view
    And I choose to 'proviso' the licence
    Then I see the fields pre-populated with the proviso and advice picklist items


  @LT_1115_grant
  Scenario: Finalise a licence
    Given I create application or application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I give myself all permissions
    And I go to application previously created
    And I click on view advice
    And I select all items in the advice view
    And I choose to 'approve' the licence
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    And I go to the team advice
    And I combine all advice
    And I go to the final advice
    And I combine all advice
    And I finalise the licence
    Then Todays date is filled in
    And I reset the permissions


  @LT_1334_finalise_goods_countries_matrix
  Scenario: Finalise goods and countries
    Given I create open application or open application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I give myself all permissions
    And I go to open application previously created
    And I click on view advice
    And I select all items in the advice view
    And I choose to 'approve' the licence
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    And I go to the team advice
    And I combine all advice
    And I go to the final advice
    And I combine all advice
    And I finalise the goods and countries
    And I click continue
    Then I see error message "Albania (Approve)"
    When I select approve for all combinations of goods and countries
    And I click continue
    Then I reset the permissions
