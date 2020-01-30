@all
Feature: View an Exhibition Clearance

  @smoke @MOD
  Scenario: View an Exhibition Clearance
    Given I go to internal homepage
    And an Exhibition Clearance is created
    When I show filters
    When filter case type has been changed to "MOD Exhibition Clearance"
    When I click on the Exhibition Clearance case
    Then I see the Exhibition Clearance case page
