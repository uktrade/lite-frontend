@notifications @all
Feature: I want to see externally visible case notes
  As a logged in exporter
  I want to view externally added case notes added by an internal gov user

  @LT-912-view
  Scenario: View a added internal case notes
    Given An application exists and a case note has been added via internal gov site
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I can see a notification
    And I click on my application
    Then I can see the internally added note
    When I go to exporter homepage
    Then I cannot see a notification