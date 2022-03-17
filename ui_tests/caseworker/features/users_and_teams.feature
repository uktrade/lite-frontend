@all @users
Feature: I want to test users

  @skip @legacy
  Scenario: Add user, deactivate then reactivate
    Given I sign in to SSO or am signed into SSO
    # Adds a new user and making sure it shows as active
    When I go to users
    When I add a new user
    And I show filters
    And I change the user filter to "Active"
    Then I see new user
    # Deactivates a new user and making sure it shows as inactive
    When I deactivate new user
    And I show filters
    And I change the user filter to "Active"
    Then I dont see new user
    When I change the user filter to "All"
    Then I see new user
    # Reactivates a new user and making sure it shows as active
    When I reactivate new user
    And I show filters
    And I change the user filter to "Active"
    Then I see new user
    When I change the user filter to "All"
    Then I see new user
    # Creates a new team and makes sure new team is in team list
    When I go to teams
    And I add a team called BlueOcean
    Then I see the team in the team list
    # Edits the new team and makes sure new team is in team list
    When I edit my team
    Then I see the team in the team list
    # Clicks on new team and makes sure user list is empty.
    When I click on the team BlueOcean
    Then I see my teams user list with user "not added"
    # Adds new user to new team.
    # Also edits the users email to make sure a user can be edited.
    When I go to users
    And I go to edit new user
    And I select my newly created team
    And I edit new users email and save
    Then the user's profile is updated
    # Makes sure the user is displayed in the new team
    When I go to teams
    And I click on the team BlueOcean
    Then I see my teams user list with user "added"
