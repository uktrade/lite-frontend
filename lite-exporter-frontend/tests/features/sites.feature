@exporter @licence @all @sitesnew
Feature: Licence
  As a...


  Scenario: Add a site
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click sites link
    When I click new site
    When I enter in text for new site " " "address" "postcode" "city" "region" and "country"
    When I click continue
    Then I see sites list

  Scenario: Edit a site
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click sites link
    When I click last edit button
    When I clear the fields for the site
    When I enter in text for new site "edited" "address edited" "pc edited" "city edited" "region edited" and "country edited"
    When I click continue
    Then I see last site name as edited
    When I click last edit button
    When I clear the fields for the site
    When I enter in text for new site " " "address" "postcode" "city" "region" and "country"


  Scenario: Test clicking continue when not adding a site
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click sites link
    When I click continue
    Then I see select a site error message

  Scenario: Test changing sites
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click sites link
    When I click new site
    When I enter in text for new site "changed" "address" "postcode" "city" "region" and "country"
    When I click continue
    Then I see sites list
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I go to exporter homepage
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click sites link
    Then I see my new site at first position
    When I select the site at position "1"
    When I click continue
    When I click sites link
    Then the checkbox I have selected at position "1" is "checked"
    When I select the site at position "1"
    Then the checkbox I have selected at position "1" is "unchecked"
    When I select the site at position "2"
    Then the checkbox I have selected at position "2" is "checked"
    When I click continue
    When I click sites link
    Then the checkbox I have selected at position "1" is "unchecked"
    Then the checkbox I have selected at position "2" is "checked"
