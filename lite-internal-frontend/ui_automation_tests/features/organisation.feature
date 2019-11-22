@internal @organisation
Feature: I want to add a company to LITE
  As a logged in government user
  I want to add a new company to LITE
  So that the new company can make applications

  @LT_934_test
  Scenario: Test organisation
    Given I go to internal homepage
    When I go to organisations
    And I choose to add a new organisation
    And I select "commercial"
    And I provide company registration details of name: "BlueOcean", EORI: "GB987654312000", SIC: "73200", VAT: "123456789", CRN: "000000011"
    And I setup an initial site with name: "HQ", address line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: "TestBusinessForSites@mail.com", first name: "Trinity", last name: "Fishburne"
    Then organisation is registered

  @LT_1417_test_adding_individual_as_organisation
  Scenario: Test registering an individual
    Given I go to internal homepage
    When I go to organisations
    And I choose to add a new organisation
    And I select "individual"
    And I provide individual registration details of first name: "Json", last name: "smith", EORI: "GB987654312000" and email: "johnsmith@email.com"
    And I setup an initial site with name: "HQ", address line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    Then organisation is registered

  @LT_1008_test_adding_hmrc_organisation
  Scenario: Test registering a HMRC organisation
    Given I go to internal homepage
    When I go to HMRC
    And I choose to add a new organisation
    And I provide hmrc registration details of org_name: "HMRC Blue", site_name: "HQ", addres line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: "TestBusinessForSites@mail.com", first name: "Trinity", last name: "Fishburne"
    And I go to organisations
    Then HMRC organisation is registered

  @LT_1086_test_adding_a_flag_to_an_organisation
  Scenario: Adding a flag to an organisation
    Given I create application or application has been previously created
    And I go to internal homepage
    When I go to flags via menu
    And I add a flag called Suspicious at level Organisation
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
