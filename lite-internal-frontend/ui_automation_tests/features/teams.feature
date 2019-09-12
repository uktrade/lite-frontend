@internal @departments
Feature: I want to add departments
  As a logged in government user
  I want to add departments
  So that an application/query can be directed to one or more departments, and progressed through those departments

  @LT_930_add
  Scenario: Add a department and then try to add same team name
    Given I go to internal homepage
    When I go to teams via menu
    And I add a team called BlueOcean
    Then I see the team in the team list

  @LT_930_click
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

  @LT_930_edit
  Scenario: Edit a department
    Given I go to teams
    When I add a team called BlueOcean
    And I edit my team
    Then I see the team in the team list
