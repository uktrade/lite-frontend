@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @LT_1376_grant @regression @LT_1760
  Scenario: Give advice and grant a licence
    Given I create application or application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click on view advice
    Then I see total goods value
    When I select all items in the advice view
    And I choose to 'approve' the licence
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    Then I see my advice has been posted successfully
    And I see added advice in the same amount of places

  @LT_1376_proviso @regression
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

  @LT_1376_deny @regression
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

  @LT_1378_pre_populate @regression
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


  @LT_1115_grant @smoke
  Scenario: Finalise a licence
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
    And I go to the team advice
    And I combine all advice
    And I go to the final advice
    And I combine all advice
    And I finalise the licence
    Then Todays date is filled in


  @LT_1334_finalise_goods_countries_matrix @regression
  Scenario: Finalise goods and countries
    Given I create open application or open application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to open application previously created
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
    Then I see country error message
    When I select approve for all combinations of goods and countries
    And I click continue

  @LT_966_refusal_flags @regression
  Scenario: Test that refusal advice is given correctly
    Given I create application or application has been previously created
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
    And I go to the team advice
    And I combine all advice
    And I go to application previously created
    Then I see refusal flag is attached
    When I click on view advice
    And I go to the team advice
    And I select all items in the advice view
    And I choose to 'approve' the licence
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    And I go to application previously created
    Then I see refusal flag is not attached
    When I click on view advice
    And I go to the team advice
    And I select all items in the advice view
    And I choose to 'refuse' the licence
    And I select decision "1a"
    And I select decision "2b"
    And I import text from the 'advice' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I click continue
    And I go to application previously created
    Then I see refusal flag is attached
    When I click on view advice
    And I go to the team advice
    And I clear advice
    And I go to application previously created
    Then I see refusal flag is not attached


  @LT_920_cannot_give_advice_terminal_case
  Scenario: Cannot give advice on a case in terminal state
    Given I create application or application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click progress application
    And I select status "Withdrawn" and save
    And I click on view advice
    Then the give advice checkboxes are not present
    And the give or change advice button is not present
    When I go to the team advice
    Then the give advice checkboxes are not present
    And the give or change advice button is not present
    When I go to the final advice
    Then the give advice checkboxes are not present
    And the give or change advice button is not present
