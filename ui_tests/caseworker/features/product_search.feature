@all @internal @product_search
Feature: I want to efficiently search for products created and used by Exporters in various applications
  As a logged in government user working on a specific case that is assigned to me
  I want to be able to search for historic product details so that I can make better
  assessment when assigning newer products on the application

  @tau_product_search
  Scenario: TAU user searching for historic product details when assessing products
    Given I sign in as "test-uat-user@digital.trade.gov.uk" # /PS-IGNORE
    And I create a standard draft application with "Product search" as reference
    And I add Consignee with details "Consignee", "1234 Export yard", "FR"
    And I add End-user with details "End user", "1234 Industrial Estate", "AU"
    And I add a set of products to the application as json:
      [
        {"name": "sporting shotgun", "part_number": "SP123", "control_list_entries": ["6A005b5b1"]},
        {"name": "Sodium chloride", "part_number": "NACL", "control_list_entries": ["PL9010"]},
        {"name": "Cleaning kit", "part_number": "PN156", "control_list_entries": ["ML1a"]},
        {"name": "Magnetic sensor", "part_number": "MAG690", "control_list_entries": ["6A006"]},
        {"name": "sporting rifle", "part_number": "SR985", "control_list_entries": ["ML22a"]}
      ]
    And the application is submitted
    When I go to application previously created
    And I assign myself to the case
    And I assign the case to "Technical Assessment Unit SIELs to Review" queue
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Technical Assessment Unit SIELs to Review"
    And I go to my case list
    Then I see previously created application
    When I click on the application previously created
    And I assign myself to the case
    Then I click on Product assessment

    # Assess products
    When I select product "sporting shotgun" to assess
    And I assess rating as "ML21a"
    And I assess report summary subject as "sporting shotguns"
    And I do not add any regimes
    And I add assessment note as "sporting shotguns"
    And I submit my assessment for this product
    Then I see "sporting shotgun" in the list of assessed products

    When I select product "Sodium chloride" to assess
    And I assess rating as "PL9011"
    And I assess report summary prefix as "technology for"
    And I assess report summary subject as "chemical mixtures"
    And I do not add any regimes
    And I add assessment note as "technology for chemical mixtures"
    And I submit my assessment for this product
    Then I see "Sodium chloride" in the list of assessed products

    When I select product "Cleaning kit" to assess
    And I assess rating as "ML4a"
    And I assess report summary subject as "accelerometers"
    And I do not add any regimes
    And I add assessment note as "accelerometers"
    And I submit my assessment for this product
    Then I see "Cleaning kit" in the list of assessed products

    When I select product "Magnetic sensor" to assess
    And I assess rating as "6A006"
    And I assess report summary subject as "accelerometers"
    And I do not add any regimes
    And I add assessment note as "magnetic sensors"
    And I submit my assessment for this product
    Then I see "Magnetic sensor" in the list of assessed products

    When I select product "sporting rifle" to assess
    And I assess rating as "ML10e2"
    And I assess report summary prefix as "components for"
    And I assess report summary subject as "accelerometers"
    And I do not add any regimes
    And I add assessment note as "components for accelerometers"
    And I submit my assessment for this product
    Then I see "sporting rifle" in the list of assessed products

    # search scenarios
    When I go to product search page

    ## suggestions
    # word prefix
    And I start typing "spo" in search field
    Then I should see "2" suggestions related to "name" with values "sporting shotgun,sporting rifle"
    And I should see "1" suggestions related to "report_summary" with values "sporting shotguns"

    # select a suggestion
    When I select suggestion for "name" with value "sporting rifle" and submit
    Then I should see below hit in search results as json:
      {
        "num_results": 1,
        "hits": [
          {
            "name": "sporting rifle",
            "part_number": "SR985",
            "Destination": ["Australia", "France"],
            "Control list entry": ["ML10e2"],
            "Regime": [],
            "Report summary": "components for accelerometers",
            "Assessment notes": "components for accelerometers",
            "Quantity": "64 items",
            "Value": "£256.32"
          }
        ]
      }

    # phrase prefix
    When I start typing "technology for" in search field
    Then I should see "1" suggestions related to "report_summary" with values "technology for chemical mixtures"

    # search string without selecting suggestions
    When I enter search string as "chemical AND mixtures" and submit
    Then I should see below hit in search results as json:
      {
        "num_results": 1,
        "hits": [
          {
            "name": "Sodium chloride",
            "part_number": "NACL",
            "Destination": ["Australia", "France"],
            "Control list entry": ["PL9011"],
            "Regime": [],
            "Report summary": "technology for chemical mixtures",
            "Assessment notes": "technology for chemical mixtures",
            "Quantity": "64 items",
            "Value": "£256.32"
          }
        ]
      }

    # Searching using Exporter suggested CLE should not give any results
    When I enter search string as "6A005b5b1" and submit
    Then I should see below hit in search results as json:
      {
        "num_results": 0,
        "hits": []
      }
    And I logout
