@all
Feature: I want to submit SIEL applications and be able to make major amendments and resubmit
  As a logged in exporter
  I want to submit SIEL applications and be able to make major amendments and resubmit

  @skip
  Scenario: Exporter making major amendments to an already submitted application
    Given I signin and go to exporter homepage and choose Test Org
    And I create a standard draft application with "Amend by copy" as reference
    When I go to task list of the draft application
    And I add Consignee with details "Consignee", "1234 Consignee address", "FR"
    And I add End-user with details "End user", "1234 End-user address", "AU"
    And I add a set of products to the application as json:
      [
        {"name": "Sporting shotgun", "part_number": "SP123", "control_list_entries": ["6A005b5b1"]},
        {"name": "Sodium chloride", "part_number": "NACL", "control_list_entries": ["PL9010"]},
        {"name": "Ammunition", "part_number": "PN156", "control_list_entries": ["ML1a"]},
        {"name": "Magnetic sensor", "part_number": "MAG690", "control_list_entries": ["6A006"]},
        {"name": "Imaging device", "part_number": "IMX300", "control_list_entries": ["ML22a"]}
      ]
    And I continue to submit application
    And I click continue
    And I agree to the declaration
    Then application is submitted
    And I record application reference code
    #
    # Edit journey
    #
    When I go to my list of applications
    And I click on the application previously submitted
    And I proceed to edit this application
    Then I see confirmation page to open application for editing 
    When I confirm to edit the application
    Then I see task list of amended application
    #
    # Status checks
    #
    When I go to my list of applications
    And I click on the application previously submitted
    Then the application cannot be opened for editing
    And the application status is "Superseded by exporter edit"
    When I go to my list of applications
    Then I see new application ready for amendments under drafts
    #
    # Products and party checks
    #
    When I go to task list of the amended draft application
    And I click on "Tell us about the products" section
    Then I see products with below details as json:
      ["Sporting shotgun", "Sodium chloride", "Ammunition", "Magnetic sensor", "Imaging device"]
    When I go to task list of the amended draft application
    And I click on "Consignee" section
    Then I see Consignee with details "Consignee", "1234 Consignee address, France"
    When I go to task list of the amended draft application
    And I click on "End user" section
    Then I see End-user with details "End user", "1234 End-user address Australia"
