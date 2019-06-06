@exporter @licence @all @submit
Feature: Licence
  As a...

  Scenario: Apply for a licence to draft
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    Then I see the application overview

  Scenario: Delete application from draft
    Given I go to exporter homepage
    When I click drafts
    When I click the application
    When I delete the application

  Scenario: Submit application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click sites link
    When I select the site at position "1"
    When I click continue
    When I click on the goods link from overview
    When I click the add from organisations goods button
    When I click add to application for the good at position "1"
    When I click continue
    Then I see enter valid quantity and valid value error message
    When I add values to my good of "1" quantity "123" and unit of measurement "Metres"
    When I click continue
    Then good is added to application
    When I click overview
    When I click on end user
    When I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    When I submit the application
    Then application is submitted
    When I go to exporter homepage
    When I click applications
    Then I see submitted application

  Scenario: Error message when there is no site selected
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click continue
    Then I see no sites attached error message

  Scenario: Error messages when not adding fields to applications
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on apply for a license button
    When I click on start button
    When I click continue
    Then error message is "Enter a reference name for your application."
    When I enter in name for application and continue
    When I click continue
    Then error message is "Select which type of licence you want to apply for."
    When I select "standard" application and continue
    When I click continue
    Then error message is "Select if you want to apply for a temporary or permanent licence."
    When I select "permanent" option and continue
    #   When I click continue
    #   Then error message is "Expected validation error for Have you been told that you need an export licence by an official? "
    #   Then error message is "Have you been told that you need an export licence by an official? "
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I delete the application
    Then I see the homepage
