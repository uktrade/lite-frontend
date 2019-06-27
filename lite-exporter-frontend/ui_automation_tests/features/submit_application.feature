  @exporter @licence @all @submit
  Feature: Licence
    As a...

  Scenario: Apply for a licence to draft
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    Then I see the application overview
    When I delete the application

  Scenario: Submit application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I add a good with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click on the goods link from overview
    And I click the add from organisations goods button
    And I click add to application for the good at position "1"
    And I click continue
    Then I see enter valid quantity and valid value error message
    When I add values to my good of "1" quantity "123" and unit of measurement "Metres"
    And I click continue
    Then good is added to application
    When I click overview
    And I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

Scenario: Submit application with external locations
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I add a good with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "external" for where my goods are located
    And I click on add new address
    And I fill in new external location form with name: "location 1", address: "London" and country: "Ukraine" and continue
    And I click on add new address
    And I fill in new external location form with name: "place", address: "Paris" and country: "Ukraine" and continue
    Then I see "2" locations
    When I click on preexisting locations
    And I select the location at position "2" in external locations list and continue
    And I click on application overview
    And I click on the goods link from overview
    And I click the add from organisations goods button
    And I click add to application for the good at position "1"
    And I add values to my good of "1" quantity "123" and unit of measurement "Metres"
    And I click continue
    Then good is added to application
    When I click overview
    And I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I submit the application
    And I click applications
    Then I see submitted application

  Scenario: Error message when there is no site selected
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click continue
    Then I see no sites or external sites attached error message

  Scenario: Error messages when not adding fields to applications
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on apply for a license button
    And I click on start button
    And I click continue
    Then error message is "Enter a reference name for your application."
    When I enter in name for application and continue
    And I click continue
    Then error message is "Select which type of licence you want to apply for."
    When I select "standard" application and continue
    And I click continue
    Then error message is "Select if you want to apply for a temporary or permanent licence."
    When I select "permanent" option and continue
    When I click continue
    Then error message is "Expected validation error for Have you been told that you need an export licence by an official? "
    Then error message is "Have you been told that you need an export licence by an official? "
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I delete the application
    Then I see the homepage
