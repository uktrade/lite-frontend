@all @internal @flags
Feature: I want to create and deactivate flags
  As a logged in government user
  I want to create and deactivate flags
  So that I can make new flags where required and prevent flags which are no longer relevant from being assigned

  @skip @legacy
  Scenario: Add, edit and deactivate a flag
    Given I sign in to SSO or am signed into SSO
    When I go to flags
    And I add a new flag with blocking approval set to "False"
    Then I see the flag in the flag list
    When I edit the flag I just made
    Then I see the flag in the flag list
    When I deactivate the flag
    And I click only show deactivated
    Then I see the flag in the flag list
    When I reactivate the flag
    Then I see the flag in the flag list


  @skip @legacy
  Scenario: Create an approval blocking flag
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I "approve" all elements of the application at user and team level
    When I go to flags
    And I add a new flag with blocking approval set to "True"
    Then I see the flag in the flag list
    When I go to application previously created
    And I click edit flags link
    And I select a previously created flag
    And I click edit flags link
    Then The previously created flag is assigned to the case
    When I go to the final advice page by url
    Then I cannot finalise the case due to the blocking flag
