@licence @sites @all
Feature: I  want to add and rename my sites
  As a logged in exporter who is admin for their organisation
  I want to add and rename sites
  So that an application can be made from one of those sites

  @LT_933_add @smoke
  Scenario: Add a site
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    And I click sites link
    And I click new site
    And I enter in text for new site " " "4 Privet Drive" "SU1 1BB" "Surrey" "Surrey" and "Ukraine"
    And I click continue
    Then I see sites list

  @LT_933_edit @regression
  Scenario: Edit a site
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    And I click sites link
    And I click the first view link
    And I click the edit button
    And I clear the fields for the site
    And I enter in text for new site "edited" "4 Privet Drive" "SU1 1BB" "Surrey" "Surrey" and "Ukraine"
    And I click continue
    Then I see last site name as edited

  @LT_933_change @regression
  Scenario: Test changing sites
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    And I click sites link
    And I click new site
    And I enter in text for new site "changed" "4 Privet Drive" "SU1 1BB" "Surrey" "Surrey" and "Ukraine"
    And I click continue
    Then I see sites list
    When I go to exporter homepage
    When I create a standard application
    And I click on application locations link
    And I select "organisation" for where my goods are located
#    Disabled step because site ordering seems not to be fixed (LT-1518)
#    Then I see my new site at first position
    When I select the site at position "1"
    And I click continue
    And I click edit sites button
    Then the checkbox I have selected at position "1" is "checked"
    When I select the site at position "1"
    Then the checkbox I have selected at position "1" is "unchecked"
    When I select the site at position "2"
    Then the checkbox I have selected at position "2" is "checked"
    When I click continue
    And I click edit sites button
    Then the checkbox I have selected at position "1" is "unchecked"
    And the checkbox I have selected at position "2" is "checked"
