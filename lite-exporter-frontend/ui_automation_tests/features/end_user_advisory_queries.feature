@end_user_advisory_queries @all
Feature: I want to raise an End User advisory enquiry to check if a particular end user/ultimate end user is a suitable end user for export
  As a logged in exporter
  I want to raise an End User advisory enquiry for a particular end user/ultimate end user
  So that I can be advised whether or not the person I am seeking to export my goods is a suitable end user for export


  @LT_1007
  Scenario: create and see listed an end user advisory
    Given I go to exporter homepage and choose Test Org
    When I click on end user advisories
    And I select to create a new advisory
    And I select "government" user type and continue
    And I select "John" for the name, "4 place" for the address, "Aruba" as the country, and continue
    And I enter "reasoning" for my reason, and "these are notes" for notes and click submit
    Then I am given a confirmed submitted page, and am shown a 10 digit code
