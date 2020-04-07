@all @internal @flags
Feature: I want to create and deactivate flags
  As a logged in government user
  I want to create and deactivate flags
  So that I can make new flags where required and prevent flags which are no longer relevant from being assigned

  @LT_950_add_edit @regression
  Scenario: Add, edit and deactivate a flag
    Given I sign in to SSO or am signed into SSO
    When I go to flags
    And I add a new flag
    Then I see the flag in the flag list
    When I edit the flag I just made
    Then I see the flag in the flag list
    When I deactivate the flag
    And I click only show deactivated
    Then I see the flag in the flag list
    When I reactivate the flag
    Then I see the flag in the flag list
