@all @internal @view_cases
Feature: I want to view the case details of a case
  As a Logged in government user
  I want to view the details on a case
  So that I can make review the case before making any decisions

  @LT_1042_can_see_all_parties @regression
  Scenario: Gov user can see all parties on the case
    Given I sign in to SSO or am signed into SSO
    And I create application or application has been previously created
    When I go to application previously created
    Then I see an end user
    And I see an ultimate end user
    And I see a third party
    And I see a consignee

  @LT_1658_parties_refactor @regression
  Scenario: Gov user can see inactive parties on case
    Given I sign in to SSO or am signed into SSO
    And I create application or application has been previously created
    And the exporter has deleted the third party
    When I go to application previously created
    Then I see an inactive party on page

  @LT_982_exporter_edited_case_anchor @LT_1180_exporter_amendments_queue @regression
  Scenario: Gov user can see exporter has made changes to case
    Given I sign in to SSO or am signed into SSO
    And I create application or application has been previously created
    And I am an assigned user for the case
    And the exporter user has edited the case
    When I go to the internal homepage
    And I click on the exporter amendments banner
    Then I can see the case on the exporter amendments queue
    When I go to application previously created
    Then I see that changes have been made to the case

    @LT_948_can_see_assigned_users @regression
    Scenario: Gov user can see which users are assigned to a case from the case screen
    Given I sign in to SSO or am signed into SSO
    And I create application or application has been previously created
    And I am an assigned user for the case
    When I go to application previously created
    Then I see assigned queues
    And I see assigned users
