@all @internal @flags
Feature:  I want to create and deactivate case flags
  As a logged in government user
  I want to create and deactivate case flags
  So that I can make new flags where required and prevent flags which are no longer relevant from being assigned to cases

  @LT_950_edit @regression
  Scenario: Edit a flag
    Given I go to internal homepage
    When I go to flags
    When I add a flag called UAE at level Case
    And I edit my flag
    Then I see the flag in the flag list

  @LT_950_deactivate @regression
  Scenario: Deactivate and reactivate a flag
    Given I go to internal homepage
    When I go to flags
    When I click include deactivated
    And I count the number of active flags
    And I deactivate the first active flag
    And I click include deactivated
    Then I see one less active flags
    When I reactivate the first deactivated flag
    And I click include deactivated
    Then I see the original number of active flags
