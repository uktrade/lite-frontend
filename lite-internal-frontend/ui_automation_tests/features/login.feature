Feature: Login

  Scenario: Invalid user
    Given I go to SSO UAT login page
    When I log in with invalid user
    And I click log in button
    And I go to the internal homepage
    Then I see you need to sign in error message

  Scenario: Empty user
    Given I go to SSO UAT login page
    When I click log in button
    And I go to the internal homepage
    Then I see you need to sign in error message