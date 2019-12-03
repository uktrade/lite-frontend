@all @internal @teams
Feature: I want to add a team
  As a logged in government user
  I want to add teams
  So that an application/query can be directed to one or more teams, and progressed through those teams

  @LT_930_add @smoke
  Scenario: Add a team
    Given I go to internal homepage
    When I go to teams via menu
    And I add a team called BlueOcean
    Then I see the team in the team list

  @LT_930_click @regression
  Scenario: Add a team and click on team name and add user to team and rollback
    Given I go to teams
    When I add a team called BlueOcean
    And I click on my team
    Then I see my teams user list with user "not added"
    When I go to users
    And I click edit for my user
    And I select my newly created team
    And I click on my team
    Then I see my teams user list with user "added"
    When I click edit for my user
    And I select Admin team

  @LT_930_edit @regression
  Scenario: Edit a team
    Given I go to teams
    When I add a team called BlueOcean
    And I edit my team
    Then I see the team in the team list
