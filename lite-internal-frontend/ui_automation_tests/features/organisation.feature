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
    And I provide company registration details of name: "BlueOcean", EORI: "GB987654312000", SIC: "73200", VAT: "123456789", CRN: "000000011"
    And I setup an initial site with name: "HQ", addres line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: "TestBusinessForSites@mail.com", first name: "Trinity", last name: "Fishburne"
    Then organisation is registered
