@goods @all
Feature: I want to archive unused goods and restore them when required again
  As a logged in exporter
  I want to add archive goods in my goods list
  So that I can better manage my products list



@goods_archive_restore
  Scenario: Archive unused goods that are submitted on an application and restore if required again
    Given I signin and go to exporter homepage and choose Test Org
    And I create a standard draft application with "Amend by copy" as reference
    When I go to task list of the draft application
    And I add Consignee with details "Consignee", "1234 Consignee address", "FR"
    And I add End-user with details "End user", "1234 End-user address", "AU"
    And I add a set of products to the application as json:
      [
        {"name": "Sensor", "part_number": "SP123", "control_list_entries": ["6A005b5b1"]},
        {"name": "Spectroscope", "part_number": "PN156", "control_list_entries": ["ML1a"]}
      ]
    And I continue to submit application
    And I click continue
    And I agree to the declaration
    Then application is submitted
    And I record application reference code
    #
    # Check product details and archive
    #
    When I go to my products list
    And I select the product "Spectroscope" from the list to view details
    Then I see an option to archive the product
    When I click to archive the product
    Then I see a confirmation page to archive the product
    When I continue to archive the product
    Then the product "Spectroscope" is archived
    And I see the product "Spectroscope" in the archived products list
    #
    # Restoring a product
    #
    When I select the product "Spectroscope" from the list to view details
    Then I see an option to restore the product
    When I click to restore the product
    Then I see a confirmation page to restore the product
    When I continue to restore the product
    Then the product "Spectroscope" is restored
    And I do not see the product "Spectroscope" in the archived products list
    #
    # Archive history checks
    #
    When I go to my products list
    And I select the product "Spectroscope" from the list to view details
    Then I see archive history for the product with "2" revisions
