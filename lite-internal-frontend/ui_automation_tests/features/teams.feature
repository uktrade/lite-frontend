@internal @departments
Feature: I want to add departments
  As a logged in government user
  I want to add departments
  So that an application/query can be directed to one or more departments, and progressed through those departments

  @LT-930_add
  Scenario: Add a department and then try to add same team name
    Given I go to internal homepage
    When I go to teams
    And I add a team called "DIT"
    Then I see the team in the team list
    When I add an existing team name
    Then I see error message "Enter a name which is not already in use by another team"

  @LT-930_click
  Scenario: Add a team and click on team name and add user to team and rollback
    Given I go to internal homepage
    When I go to teams
    And I add a team called "DIT"
    When I click on my team
    Then I see my teams user list with user "not added"
    When I go to users
    And I click edit for my user
    And I select my newly created team
    And I click on my team
    Then I see my teams user list with user "added"
    When I click edit for my user
    And I select Admin team

  @LT-930_empty
  Scenario: Add a department with empty field
    Given I go to internal homepage
    When I go to teams
    And I add a team called " "
    Then I see error message "Team name may not be blank"

  @LT-930_too_many
  Scenario: Add a department with over 50 characters field
    Given I go to internal homepage
    When I go to teams
    And I add a team called "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    Then I see error message "Ensure this field has no more than 50 characters."

  @LT-930_edit
  Scenario: Edit a department
    Given I go to internal homepage
    When I go to teams
    And I add a team called "Team to edit"
    And I edit my team
    Then I see the team in the team list
