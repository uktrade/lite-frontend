@all @internal @organisation
Feature: I want to add a company to LITE
  As a logged in government user
  I want to add a new company to LITE
  So that the new company can make applications

  @LT_934_test @smoke
  Scenario: Test registering an organisation
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new commercial organisation
    Then organisation is registered
    When I edit an organisation
    Then organisation is edited

  @LT_1417_test_adding_individual_as_organisation @regression
  Scenario: Test registering an individual
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new individual organisation
    Then individual organisation is registered

  @LT_1008_test_adding_hmrc_organisation @regression
  Scenario: Test registering a HMRC organisation
    Given I sign in to SSO or am signed into SSO
    When I go to HMRC
    And I add a new HMRC organisation
    And I go to organisations
    Then HMRC organisation is registered

  @LT_1086_test_adding_a_flag_to_an_organisation @regression
  Scenario: Adding a flag to an organisation
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I go to flags
    And I add a flag at level Organisation
    And I go to application previously created
    And I go to the organisation which submitted the case
    And I click the edit flags link
    And I select previously created flag
    Then the previously created organisations flag is assigned
    When I go to open application previously created
    Then the previously created organisations flag is assigned
    When I go to the internal homepage
    Then I see previously created application
    And I see the added flags on the queue
