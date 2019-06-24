@exporter @licence @all @sitesnew
Feature: Licence
  As a...


  Scenario: Add a site
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click sites link
    And I click new site
    And I enter in text for new site " " "address" "postcode" "city" "region" and "country"
    And I click continue
    Then I see sites list

  Scenario: Edit a site
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click sites link
    And I click last edit button
    And I clear the fields for the site
    And I enter in text for new site "edited" "address edited" "pc edited" "city edited" "region edited" and "country edited"
    And I click continue
    Then I see last site name as edited
    When I click last edit button
    And I clear the fields for the site
    And I enter in text for new site " " "address" "postcode" "city" "region" and "country"


  Scenario: Test clicking continue when not adding a site
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click continue
    Then I see select a site error message

  Scenario: Test changing sites
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click sites link
    And I click new site
    And I enter in text for new site "changed" "address" "postcode" "city" "region" and "country"
    And I click continue
    Then I see sites list
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "organisation" for where my goods are located
    Then I see my new site at first position
    When I select the site at position "1"
    And I click continue
    And I click on application locations link
    And I select "organisation" for where my goods are located
    Then the checkbox I have selected at position "1" is "checked"
    When I select the site at position "1"
    Then the checkbox I have selected at position "1" is "unchecked"
    When I select the site at position "2"
    Then the checkbox I have selected at position "2" is "checked"
    When I click continue
    And I click on application locations link
    And I select "organisation" for where my goods are located
    Then the checkbox I have selected at position "1" is "unchecked"
    And the checkbox I have selected at position "2" is "checked"
