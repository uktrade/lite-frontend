@licence @submit @all
Feature: I want to indicate the kind of licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  @LT-1091_draft
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

  @LT-1091_standard
  Scenario: Submit standard application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    When I click add a good button
    And I add a good or good type with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
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
    #Commenting out following steps due to bug - LT-1287 - uncomment when this is fixed
    # And I click continue
    # Then I see enter valid quantity and valid value error message
    And I add values to my good of "1" quantity "123" and unit of measurement "Metres"
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

  @LT-1091_external
  Scenario: Submit application with external locations
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I click add a good button
    And I add a good or good type with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
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

  @LT-1114
  Scenario: Submit open application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I click add a good button
    And I add a good or good type with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on application locations link
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click on the goods link from overview
    And I click Add goods type button
    And I add a good or good type with description "Good Type T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "empty"
    Then I see my goods type added at position "1" with a description and a control code
    When I click overview
    Then I see my goods type added to the overview page with a description and a control code
    When I click on the goods link from overview
    And I click Add goods type button
    And I click continue
    Then I see good types error messages
    When I add a good or good type with description "Good Type T2" controlled "Yes" control code "1234" incorporated "Yes" and part number "empty"
    Then I see my goods type added at position "2" with a description and a control code
    When I click overview
    Then I see my goods type added to the overview page with a description and a control code
    When I click on countries
    Then I should see a list of countries
    When I select "Canada" from the country list
    And I select "Poland" from the country list
    And I select "United Kingdom" from the country list
    And I click continue
    Then I can see "3" countries selected on the overview page
    When I click on number of countries on the overview page
    Then I see "Canada" in a modal
    And I see "Poland" in a modal
    And I see "United Kingdom" in a modal
    When I close the modal
    And I submit the application
    Then application is submitted
    When I go to exporter homepage
    And I click applications
    Then I see submitted application

  @LT-1092_search
  Scenario: Search for countries
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on countries
    And I search for country "Canada"
    Then only "Canada" is displayed in country list

  @LT-1092_error
  Scenario: Error message when not adding countries
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on goods link
    And I click add a good button
    And I add a good or good type with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
    And I go to exporter homepage
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click on countries
    And I click continue
    Then error message is "You have to pick at least one country"

  @LT-1091_no_site_selected
  Scenario: Error message when not adding goods and sites information for standard application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "standard" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click continue
    Then I see no sites external sites or end user attached error message

  @LT-1114_error
  Scenario: Error message when not adding goods and sites information for open application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on apply for a license button
    And I click on start button
    And I enter in name for application and continue
    And I select "open" application and continue
    And I select "permanent" option and continue
    And I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    And I click continue
    Then I see no sites good types or countries attached error message

  @LT-1091_no_fields
  Scenario: Error messages when not adding fields to applications
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    And I click on apply for a license button
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
