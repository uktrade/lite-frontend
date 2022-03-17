@all @internal @copied_applications
Feature: I want to see that a copied application references the previous application

  @skip @legacy
  Scenario: View original application link in new application
    Given I sign in to SSO or am signed into SSO
    And I have an open application from copying
    When I go to application previously created
    Then I can see the original application is linked
    When I go to the case list page
    Then I should see my case in the cases list
    And I should see my case SLA
