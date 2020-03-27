@licence @sites @all
Feature: I  want to add and rename my sites
  As a logged in exporter who is admin for their organisation
  I want to add and rename sites
  So that an application can be made from one of those sites

  @LT_933_add_edit_site @regression
  Scenario: Add and edit a site
    Given I go to exporter homepage and choose Test Org
    When I click on the manage my organisation link
    And I click sites link
    And I click new site
    And I specify that my site is in the United Kingdom
    And I enter in the site details
    And I assign all users
    Then the site is created
    When I click the change name link
    And I change the site name
    Then the site is updated
