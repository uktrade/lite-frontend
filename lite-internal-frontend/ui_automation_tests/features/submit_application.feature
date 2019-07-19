@exporter @all @setup @document_upload
Feature: Set up application

  @submit_app
  Scenario: Submit application
    Given I go to exporter homepage
    When I login to exporter homepage with username "trinity@unicorns.com" and "12345678900"
    And I click on goods tile
    And I add a good with description "MPG 2.0" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
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
    And I add values to my good of "1" quantity "123" and unit of measurement "Metres"
    And I click continue
    Then good is added to application
    When I click overview
    And I click on end user
    And I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I submit the application
    Then application is submitted
