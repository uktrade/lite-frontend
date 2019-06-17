@internal @set_up  @all
Feature: Manage cases
As a...

  Scenario: Manage cases
    Given I go to internal homepage
    When I go to cases view
    Then cases are shown