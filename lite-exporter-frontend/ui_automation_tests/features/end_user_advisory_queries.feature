@end_user_advisory_queries @all
Feature: I want to raise an End User advisory enquiry to check if a particular end user/ultimate end user is a suitable end user for export
  As a logged in exporter
  I want to raise an End User advisory enquiry for a particular end user/ultimate end user
  So that I can be advised whether or not the person I am seeking to export my goods is a suitable end user for export

  @LT_1007 @LT_1483 @smoke
  Scenario: create an end user advisory and copy an existing end user advisory
    Given I go to exporter homepage and choose Test Org
    When I click on end user advisories
    And I select to create a new advisory
    And I select "commercial" user type and continue
    And I enter "Love heart systems" for the name
    And I enter "Love hearts" for the nature of business
    And I enter "John" for the primary contact name, "director" for primary contact_job_title, "john@email.com" for the primary contact email, "123456789" for the primary contact telephone
    And I enter "4 place" for the address, "Aruba" as the country and continue
    And I enter "reasoning" for my reason, and "these are notes" for notes and click submit
    When I go to exporter homepage
    And I click on end user advisories
    And I click copy on an existing end user advisory
    And I enter "Matt" for the name and continue
    And I enter "reasoning" for my reason, and "these are notes" for notes and click submit

  @LT_1474_case_notes @regression
  Scenario: can view gov users case note, and can submit own case note
    Given An end user advisory with a case note has been added via gov user
    And I go to exporter homepage and choose Test Org
    When I click on end user advisories
#   TODO Uncomment (flaky)
#   Then I see a notification on end user advisory list
    When I open an end user advisory already created
    Then I see a notification for case note and can view the case note
    When I enter "This is my new case note" for case note
    And I click post note
    Then I can view "This is my new case note" in case notes

  @LT_1474_ecju_queries @regression
  Scenario: can view and respond to ecju queries
    Given An end user advisory with an ecju query has been added via gov user
    And I go to exporter homepage and choose Test Org
    When I click on end user advisories
    Then I see a notification on end user advisory list
    When I open an end user advisory already created
    And I click the ECJU Queries tab
    And I click to respond to the ecju query
    And I enter "This is my response" for ecju query and click submit
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed
