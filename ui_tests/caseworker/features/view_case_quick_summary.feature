@all @internal @view_quick_summary
Feature: I want to be able to view the quick summary on a case

  Scenario: View quick summary page
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I click the text "Quick summary"
    Then I see the quick summary
    And I logout
