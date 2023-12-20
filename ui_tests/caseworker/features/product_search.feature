@all @internal @product_search
Feature: I want to efficiently search for products created and used by Exporters in various applications
  As a logged in government user working on a specific case that is assigned to me
  I want to be able to search for historic product details so that I can make better
  assessment when assigning newer products on the application

  @tau_product_search
  Scenario: TAU user searching for historic product details when assessing products
    Given I sign in to SSO or am signed into SSO
    And I create a standard draft application with "Product search" as reference
    And I add Consignee with details "Consignee", "1234 Export yard", "FR"
    And I add End-user with details "End user", "1234 Industrial Estate", "AU"
    And I add a set of products to the application as json:
      [
        {"name": "sporting shotgun", "part_number": "SP123", "control_list_entries": ["ML22a"]},
        {"name": "Sodium chloride", "part_number": "NACL", "control_list_entries": ["PL9010"]},
        {"name": "Cleaning kit", "part_number": "PN156", "control_list_entries": ["ML1a"]},
        {"name": "Magnetic sensor", "part_number": "MAG690", "control_list_entries": ["6A006"]},
        {"name": "sporting rifle", "part_number": "SR985", "control_list_entries": ["ML22a"]}
      ]
    And the application is submitted
    And I add my assessment as TAU case advisor as json:
      [
        {"control_list_entries": ["ML21a"], "regime_entries": ["586c5ce7-30f0-4873-ad1b-652eaf40ebff"], "report_summary_prefix": "", "report_summary_subject": "e97ffe1a-d198-415d-98b6-93d2b191760b", "comment": "sporting shotguns"},
        {"control_list_entries": ["PL9011"], "regime_entries": [], "report_summary_prefix": "ca6a7b52-84cf-4c32-a608-bed74f43f085", "report_summary_subject": "b8fb9c5d-21b6-4de7-b24b-7357ce00269f", "comment": "technology for chemical mixtures"},
        {"control_list_entries": ["ML4a"], "regime_entries": [], "report_summary_prefix": "", "report_summary_subject": "289f548f-bf07-448d-8042-36a5b10fd5f5", "comment": ""},
        {"control_list_entries": ["6A006"], "regime_entries": [], "report_summary_prefix": "", "report_summary_subject": "289f548f-bf07-448d-8042-36a5b10fd5f5", "comment": ""},
        {"control_list_entries": ["ML10e2"], "regime_entries": [], "report_summary_prefix": "42e813cb-a75c-4f60-a121-dbe949222dd8", "report_summary_subject": "289f548f-bf07-448d-8042-36a5b10fd5f5", "comment": "components for accelerometers"}
      ]
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Technical Assessment Unit SIELs to Review"

    # search scenarios
    And I go to product search page

    ## suggestions
    # word prefix
    And I start typing "spo" in search field
    Then I should see "2" suggestions related to "name" with values "sporting shotgun,sporting rifle"
    And I should see "1" suggestions related to "report_summary" with values "sporting shotguns"

    # select a suggestion
    When I select suggestion for "name" with value "sporting rifle" and submit
    Then I see below search results as json:
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
    Then I see below search results as json:
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

    # search using regime
    When I enter search string as "wassenaar" and submit
    Then I see below search results as json:
      {
        "num_results": 1,
        "hits": [
          {
            "name": "sporting shotgun",
            "part_number": "SP123",
            "Destination": ["Australia", "France"],
            "Control list entry": ["ML21a"],
            "Regime": ["W"],
            "Report summary": "sporting shotguns",
            "Assessment notes": "sporting shotguns",
            "Quantity": "64 items",
            "Value": "£256.32"
          }
        ]
      }

    # Searching using Exporter suggested CLE should not give any results
    When I enter search string as "ML22a" and submit
    Then I see below search results as json:
      {
        "num_results": 0,
        "hits": []
      }
