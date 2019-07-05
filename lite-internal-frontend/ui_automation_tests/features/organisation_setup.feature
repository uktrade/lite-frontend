@internal @setup @organisation
Feature: I want to add a company to LITE
As a logged in government user
I want to add a new company to LITE
So that the new company can make applications

  @LT-934_set_up
  Scenario: Set up organisation
    Given I go to internal homepage
    When I go to organisations
    And I choose to add a new organisation for setup
    And I provide company registration details of name: "Unicorns Ltd", EORI: "1234567890AAA", SIC: "2345", VAT: "GB1234567", CRN: "09876543"
    And I setup an initial site with name: "Headquarters", addres line 1: "42 Question Road", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: "trinity@unicorns.com", first name: "Trinity", last name: "Fishburne", password: "12345678900"
    Then organisation is registered

  @LT-934_test
  #These are identical but the reason they are both still there is because the first one is a setup task, so only runs if the email doesnt already exist, the second is to test the functionality so it will always run.
  Scenario: Test organisation
    Given I go to internal homepage
    When I go to organisations
    And I choose to add a new organisation
    And I provide company registration details of name: "Test Business T", EORI: "GB987654312000", SIC: "73200", VAT: "123456789", CRN: "000000011"
    And I setup an initial site with name: "Site 1", addres line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: "TestBusinessForSites@mail.com", first name: "Trinity", last name: "Fishburne", password: "12345678900"
    Then organisation is registered
    When I go to exporter homepage
    And I login to exporter homepage with username "TestBusinessForSites@mail.com" and "12345678900"
    And I click sites link
    And I click new site
    And I enter in text for new site "Site 2" "address" "postcode" "city" "region" and "Ukraine"
    And I click continue
    And I go to the internal homepage
    And I go to organisations
    And I click on my registered organisation
    Then my new site is displayed

  @LT-934_error
  Scenario: Organisation registration validation
    Given I go to internal homepage
    When I go to organisations
    And I choose to add a new organisation
    And I provide company registration details of name: " ", EORI: " ", SIC: " ", VAT: " ", CRN: " "
    Then I see error message "This field may not be blank."
    When I provide company registration details of name: "Test Business ABC", EORI: "GB987654312000", SIC: "73200", VAT: "123456789", CRN: "000000011"
    And I setup an initial site with name: " ", addres line 1: " ", town or city: " ", County: " ", post code: " ", country: " "
    Then I see error message "This field may not be blank."
    When I setup an initial site with name: "Site 1", addres line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: " ", first name: " ", last name: " ", password: " "
    Then I see error message "This field may not be blank."
    When I setup the admin user with email: "TestBusinessABC@mail.com", first name: "Trinity", last name: "Fishburne", password: "12345678900"
    Then organisation is registered
