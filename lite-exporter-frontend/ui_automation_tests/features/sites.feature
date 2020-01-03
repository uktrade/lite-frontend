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
    When I click the first view link
    And I click the edit button
    And I clear the fields for the site
    And I enter in text for new site "edited" "4 Privet Drive" "SU1 1BB" "Surrey" "Surrey" and "Ukraine"
    And I click continue
    Then I see last site name as edited
