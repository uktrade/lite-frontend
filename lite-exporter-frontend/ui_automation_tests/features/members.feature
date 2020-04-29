@users @all
Feature: I want to manage my organisation's members
  As a logged in exporter
  I want to manage my members
  So that an application/query can be managed by only active members of staff and new members of staff can be added and their details can be kept up to date

  @LT_1177 @add_and_edit_member @regression
  Scenario: Add user, deactivate, then reactivate
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    And I add a member to the organisation
    And I show filters
    And filter status has been changed to "Active"
    Then I see the new member
    When I select the member that was just added
    And I deactivate them
    Then the member is deactivated
    When I go back to the members page
    And I show filters
    And filter status has been changed to "Active"
    Then I do not see the new member
    When filter status has been changed to "All"
    Then I see the new member
    When I select the member that was just added
    And I reactivate them
    Then the member is reactivated
    When I go back to the members page
    And I show filters
    And filter status has been changed to "Active"
    Then I see the new member
    When filter status has been changed to "All"
    Then I see the new member
    When I select the member that was just added
    And I change what sites they're assigned to
    And I change their role to Super User
    Then role is changed

