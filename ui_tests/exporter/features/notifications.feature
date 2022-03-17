@notifications @all
Feature: I want to see externally visible case notes
  As a logged in exporter
  I want to view externally added case notes added by an internal gov user

  @skip @legacy
  Scenario: View an added internal case note
    Given I go to exporter homepage and choose Test Org
    And an application exists a case note and an ecju query have been added via internal gov site
    When I go to exporter homepage
    And I click on applications
    Then I see "2" notifications on application list
    When I click on my application
    And I click the notes tab
    Then I can see the internally added note
    When I go to exporter homepage
    And I click on applications
    Then I see "1" notifications on application list
