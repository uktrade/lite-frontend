@ogel @all
Feature: I want to register for an OGL for my organisation
As a logged in exporter
I want to use LITE to register for OGEL, OGTCL and OGTL licences
So that I can register for all types of OGL

  @skip @legacy
  Scenario: Create an ogel
    Given I go to exporter homepage and choose Test Org
    And an ogel licence has been added
    When I search for an ogel application of type "ML1a" for "United Kingdom"
    And I select the created OGEL
    And I agree to the ogel declaration
    Then application is submitted
    When I go to the licences page
    And I go to the OGEL tab
    Then I see my OGEL displayed
