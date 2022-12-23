@all @internal @view_goods
Feature: I want to be able to view goods on a case

  Scenario: View goods detail page
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign the case to "FCDO Cases to Review" queue
    And I go to my profile page
    And I change my team to "FCDO" and default queue to "FCDO Cases to Review"
    And I go to my case list
    And I click the application previously created
    And I click the first good on the case
    Then I see the good details
