@exporter @all
Feature: Go to each item from the homepage

  @verify_build
  Scenario: Go to each item from the homepage
    Given I go to exporter homepage and choose Test Org
    When I refresh the page
    Then the log out link is displayed
    When I click on applications
    Then the log out link is displayed
    When I go to exporter homepage
    And I click on goods link
    Then the log out link is displayed
    When I go to exporter homepage
    And I click on end user advisories
    Then the log out link is displayed
    When I go to exporter homepage
    And I click on the manage my organisation link
    Then the log out link is displayed
