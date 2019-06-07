@internal @set_up  @all @organisation
Feature: Set up a organisation
As a...

  Scenario: Set up organisation
    Given I go to internal homepage
    When I register a new organisation
    Then organisation is registered