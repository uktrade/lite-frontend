@users @all
Feature: I want to manage my organisation's members
  As a logged in exporter
  I want to manage my members
  So that an application/query can be managed by only active members of staff and new members of staff can be added and their details can be kept up to date

  @LT_937_setup @add_and_edit_member @smoke
  Scenario: Add a new member to my organisation
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    And I add a member to the organisation
    And I select the member that was just added
    # Edit the user
    And I deactivate them, then the member is deactivated
    And I reactivate them, then the member is reactivated
    And I change what sites they're assigned to
    Then I change their role

  @deactivate_oneself @regression
  Scenario: Deactivate oneself
    Given I go to exporter homepage and choose Test Org
    When I try to deactivate myself I cannot
