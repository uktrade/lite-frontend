@notifications @all
Feature: I want to see externally visible case notes
  As a logged in exporter
  I want to view externally added case notes added by an internal gov user

  @LT_912_view
  Scenario: View an added internal case notes
    Given I go to exporter homepage
    And an application exists and a case note has been added via internal gov site
    When I go to exporter homepage
    Then I can see a notification in application tile
    When I click on applications
    Then I see a notification on application list
    When I click on my application
    Then I can see the internally added note
    When I go to exporter homepage
    Then I cannot see a notification