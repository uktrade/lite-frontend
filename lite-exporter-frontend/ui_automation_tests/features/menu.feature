@exporter @all
Feature: Go to each item from the homepage

  @verify_build
  Scenario: Go to each item from the homepage
    Given I go to exporter homepage and choose Test Org
    When I refresh the page
    Then I get a 200 and log out link is displayed
    When I click on applications
    Then I get a 200 and log out link is displayed
    When I go to exporter homepage
    And I click on goods link
    Then I get a 200 and log out link is displayed
    When I go to exporter homepage
    And I click on end user advisories
    Then I get a 200 and log out link is displayed
    When I go to exporter homepage
    And I click on the manage my organisation link
    Then I get a 200 and log out link is displayed
