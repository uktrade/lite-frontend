@all @internal @view_goods
Feature: I want to be able to view goods on a case

  Scenario: View goods detail page
    Given I sign in as Test UAT user
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I click the first good on the case
    Then I see the good details
