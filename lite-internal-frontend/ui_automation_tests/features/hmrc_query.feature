Feature: Add a HMRC query


  Scenario: Add a HMRC query
    Given I go to internal homepage
    When I show filters
    When filter case type has been changed to "HMRC Query"
    When I go to HMRC query
    Then I see HMRC query

