@licence @submit @all @standard
Feature: I want to indicate the standard licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT_1091_draft
  Scenario: Apply for a licence to draft and delete
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    Then I see the application overview
    When I delete the application

  @LT_1091_standard @setup
  Scenario: Submit standard application
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I add a non incorporated good to application
    Then good is added to application
    When I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    Then I see end user on overview
    When I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1091_external
  Scenario: Submit standard application with external locations
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "external" for where my goods are located
    And I click on add new address
    And I fill in new external location form with name: "32 Lime Street", address: "London" and country: "Ukraine" and continue
    And I click on add new address
    And I fill in new external location form with name: "place", address: "1 Paris Road" and country: "Ukraine" and continue
    Then I see "2" locations
    When I click on preexisting locations
    And I select the location at position "2" in external locations list and continue
    And I click on application overview
    And I add a non incorporated good to application
    Then good is added to application
    When I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I submit the application
    And I click applications
    Then I see submitted application

  @LT_1042_happy_path
  Scenario: Apply for a licence with ultimate end users
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on ultimate end users
    And I click on ultimate end users add button
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I click on ultimate end users add button
    And I add an end user of type: "commercial", name: "Mr Jones", website: " ", address: "London" and country "Ukraine"
    And I remove an ultimate end user so there is one less and return to the overview
    Then there is only one ultimate end user
    When I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT_1091_no_fields
  Scenario: Error messages when not adding fields to applications
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I click continue
    Then error message is "Enter a reference name for your application"
    When I enter in name for application and continue
    And I click continue
    Then error message is "Select which type of licence you want to apply for"
    When I select "standard" application and continue
    And I click continue
    Then error message is "Select if you want to apply for a temporary or permanent licence"
    When I select "permanent" option and continue
    And I click continue
    Then error message is "Select if you you been told that you need an export licence by an official"
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I delete the application
    Then I see the homepage

  @LT_1091_external_validation
  Scenario: Error messages with external empty validation
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "external" for where my goods are located
    And I click on add new address
    And I fill in new external location form with name: " ", address: " " and country: " " and continue
    Then error message is "This field may not be blank."

  @LT_1091_end_user_validation
  Scenario: Error messages with end user empty validation
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on end user
    And I click continue
    Then error message is "This field is required."
    When I add end user of type: "commercial"
    And I add end user of name: " "
    Then error message is "This field may not be blank."
    When I add end user of name: "Mr Smith"
    When I add end user of website "www.afas.com"
    Then error message is "Enter a valid URL."
    When I add end user of website " "
    When I add end user of address: " " and country " "
    Then error message is "This field may not be blank."
    When I add end user of address: "123 Home Street" and country "Ukraine"
    # Todo following step commented out due to bug
    # Then I see end user on overview

  @LT_1042_unhappy_path
  Scenario: Apply for a licence with ultimate end users error message
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on ultimate end users
    And I click on back to overview
    And I click continue
    Then I see no ultimate end user attached error message

  @LT_1114_error_when_no_goods_or_sites
  Scenario: Apply for a licence with goods and sites error message
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click continue
    Then I see no goods external sites or end user attached error message

  @LT_928_error_message
  Scenario: Error message for empty quantities.
    Given I go to exporter homepage and choose Test Org
    When I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on the goods link from overview
    And I click the add from organisations goods button
    And I click add to application for the good at position "1"
    And I click continue
    Then I see enter valid quantity and valid value error message
