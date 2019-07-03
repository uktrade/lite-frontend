@internal @set_up @organisation @all
Feature: Set up a organisation

  @set_up_org
  Scenario: Set up organisation
    Given I go to internal homepage
    When I register a new organisation
    Then organisation is registered