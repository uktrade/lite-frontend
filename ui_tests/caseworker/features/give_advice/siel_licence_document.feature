@all @internal @product_search
Feature: I want process an SIEL application submitted by Exporters and issue licence if it meets licensing criteria
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that I can issue licence and generate licence documents

  @siel_pdf
  Scenario: LU user giving final recommendation and generating licence pdf document
    Given I sign in to SSO or am signed into SSO
    And I create a standard draft application with "SIEL Licence PDF check" as reference
    And I add Consignee with details "Consignee", "1234 Export yard", "FR"
    And I add End-user with details "End user", "1234 Industrial Estate", "AU"
    And I add a set of products to the application as json:
      [
        {"name": "sporting shotgun", "part_number": "SP123", "firearm_details": {"type": "firearms", "serial_numbers": ["12345", "SN123"]}},
        {"name": "Sodium chloride", "part_number": "NACL", "control_list_entries": ["PL9010"]},
        {"name": "Cleaning kit", "part_number": "PN156", "control_list_entries": ["ML1a"]},
        {"name": "Magnetic sensor", "part_number": "MAG690", "control_list_entries": ["6A006"]},
        {"name": "sporting rifle", "part_number": "SR985", "control_list_entries": ["ML22a"]}
      ]
    And the application is submitted

    # Case progress on the Case worker side
    When I switch to "Licensing Reception" with queue "Licensing Reception SIEL applications" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Enforcement Unit Cases to Review, Technical Assessment Unit SIELs to Review"
    # EU
    When I switch to "Enforcement Unit" with queue "Enforcement Unit Cases to Review" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Technical Assessment Unit SIELs to Review"
    And I see the case is not assigned to queues "Enforcement Unit Cases to Review"

    When I go to my profile page
    And I change my team to "Admin" and default queue to "All cases"
    And I go to my case list
    And I click on the application previously created
    And I click edit flags link
    And I remove "Enforcement Check Req" flag and submit

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
    And I select product is not on the control list
    And I do not add any regimes
    And I add assessment note as "no licence required"
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
    And I select product is not on the control list
    And I assess report summary subject as "accelerometers"
    And I do not add any regimes
    And I add assessment note as "no licence required"
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

    When I click move case forward
    Then I don't see previously created application
    # LU
    When I switch to "Licensing Unit" with queue "Licensing Unit Pre-circulation Cases to Review" and I submit the case
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "MOD-DSR Cases to Review, MOD-CapProt cases to review, FCDO Cases to Review"

    # MOD-DSR
    When I switch to "MOD-DSR" with queue "MOD-DSR Cases to Review" and I submit the case
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "MOD-CapProt cases to review, FCDO Cases to Review"
    # MOD-CapProt
    When I switch to "MOD-CapProt" with queue "MOD-CapProt cases to review" and I submit the case
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "FCDO Cases to Review"
    # FCDO
    When I switch to "FCDO" with queue "FCDO Cases to Review" and I submit the case
    And I switch to "FCDO" with queue "FCDO Counter-signing" and I submit the case with decision "decision"
    Then I see the case status is now "OGD Advice"
    And I see the case is assigned to queues "Review and combine"
    When I switch to "MOD-ECJU" with queue "Review and combine" and I submit the case with decision "decision"
    Then I see the case status is now "Under final review"
    And I see the case is assigned to queues "Licensing Unit Post-circulation Cases to Finalise"

    When I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I assign myself to the case
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I enter "No concerns to issue licence" as the reasons for approving
    And I enter "subject to following conditions" as the licence condition
    And I click submit recommendation
    Then I see "No concerns to issue licence" as the reasons for approving
    And I see "subject to following conditions" as the licence condition
    When I click "Finalise case"
    And I click save
    And I start generating licence approval document
    And I select the template "SIEL template"
    And I click continue
    And I click preview
    Then I see the licence number on the SIEL licence preview
    And I check that licence is valid for "2" years
    And I check that export type is "Permanent"
    And I check that consignee details as "Consignee", "1234 Export Yard", "France"
    And I check that end-user details as "End user", "1234 Industrial Estate", "Australia"
    And I check that licence document contains "3" products
    And I check that product "1" name is "sporting shotgun", part number "SP123", serial numbers "12345,SN123"
    And I check that product "1" control entries are "ML21a", value "£256.32", quantity "64.0 Items"
    And I check that product "2" name is "Cleaning kit", part number "PN156", no serial numbers
    And I check that product "2" control entries are "ML4a", value "£256.32", quantity "64.0 Items"
    And I check that product "3" name is "sporting rifle", part number "SR985", no serial numbers
    And I check that product "3" control entries are "ML10e2", value "£256.32", quantity "64.0 Items"
    And I check that licence has additional conditions as "subject to following conditions"
    When I click continue
    Then licence approval document is generated
    When I start generating no licence required document
    And I select the template "No licence required letter template"
    And I click continue
    And I click preview
    Then I check that no licence required letter contains "2" products
    And I check that NLR product "1" name is "Sodium chloride", part number "NACL"
    And I check that NLR product "2" name is "Magnetic sensor", part number "MAG690"
    When I click continue
    Then NLR letter is generated
    When I click save and publish to exporter
    And I click on "Details" tab
    Then I see the case status is now "Finalised"
    And I see the case is not assigned to any queues
