@licence @submit @all @standard
Feature: I want to indicate the standard licence I want
  As a logged in exporter
  I want to indicate the kind of licence I want
  So that I am more likely to get the correct kind of licence or the kind of licence I would like

  Scenario: Submit standard application
    Given I signin and go to exporter homepage and choose Test Org
    When I click apply
    And I select export licence
    And I select SIEL
    And I enter "application1" as name
    And I select "no" to receiving a letter
    And I click on "Tell us about the products"
    And I click on "Add a new product"
    And I select product type "Firearm"
    And I enter "1" for number of items
    And I choose to enter serial numbers now
    And I enter "12345" for the serial numbers
    And I enter "name" as name, "ML1a" for control list, and "no it doesn’t need one" for security grading
    And I enter "2015" as the year of manufacture
    And I select "no" to a replica firearm
    And I enter ".22" as the calibre
    And I select "no" to registered firearms dealer
    And I select "I don't know" to section 1 of the firearms act
    And I click on "Continue"
    And I select no to product document and enter "reason"
    And I enter "20" as value, "no" for incorporation, "no" for deactivation, and "yes" for proof marks
    And I click on "Back to application overview"
    And I click on "End use details"
    And I enter "end use details" for the intended end use
    And I select "no" to informed by ECJU to apply
    And I select "no" to informed by ECJU about WMD use
    And I select "no" to suspected WMD use
    And I select "no" to products received under transfer licence from the EU
    And I click save and continue
    And I click on "Provide product location and journey"
    And I select "Great Britain" to where products begin export journey
    And I select "yes" to permanently exported
    And I select "yes" to shipping air waybill or lading
    And I select "directly to the end-user" to who products are going
    And I click on "Submit"
    And I click on "End user"
    And I select "no" to reusing an existing party
    And I select "commercial organisation" as the type of end user
    And I enter the "Joe Bloggs" as end user name
    And I click continue
    And I enter "123 Main Street" and "France" for end user address
    And I enter "Joe Bloggs" for signatory name
    And I select no and enter "reason" for end user document
    And I click on "Submit"
    And I submit the application
    Then my answers are played back to me
    And I see "Standard Individual Export Licence" as the Licence
    And I see "Standard Licence" as the type
    And I see "application1" as reference name
    And I see "No" as informed to apply
    And I see "Great Britain" as product journey origin
    And I see "Yes" as product permanently exported
    And I see "Yes" as way bill
    And I see "Direct to end user" as who are the products going to
    And I see "name" as name
    And I see "N/A" as part number
    And I see "Yes" as controlled
    And I see "ML1a" as control list entry
    And I see "No" as incorporated
    And I see "1 item" as quantity
    And I see "£20.00" as value
    And I see "end use details" as intended end use
    And I see "No" for informed to apply
    And I see "No" for informed WMD
    And I see "No" for suspect WMD
    And I see "No" for EU transfer
    And I see "Joe Bloggs" for end user name
    And I see "Commercial Organisation" for type
    And I see "123 Main Street, France" as address
    And I see "N/A" as website
    And I see "Joe Bloggs" as signatory
    And I see "No, I do not have an end-user undertaking or stockist undertaking" for end user document
    And I see "reason" for the explanation
    And I see "No information added to this section." for "Consignee"
    And I see "No information added to this section." for "Third parties"
    And I see "No information added to this section." for "Supporting documents"
    And I see "No information added to this section." for Notes
    When I click continue
    And I agree to the declaration
    Then application is submitted
    When I go to exporter homepage


  @serial_numbers_later
  Scenario: Submit standard application when serial numbers are not available
    Given I signin and go to exporter homepage and choose Test Org
    When I click apply
    And I select export licence
    And I select SIEL
    And I enter "application1" as name
    And I select "no" to receiving a letter
    And I click on "Tell us about the products"
    And I click on "Add a new product"
    And I select product type "Firearm"
    And I enter "4" for number of items
    And I choose to add serial numbers later
    And I enter "name" as name, "ML1a" for control list, and "no it doesn’t need one" for security grading
    And I enter "2015" as the year of manufacture
    And I select "no" to a replica firearm
    And I enter ".22" as the calibre
    And I select "no" to registered firearms dealer
    And I select "I don't know" to section 1 of the firearms act
    And I click on "Continue"
    And I select no to product document and enter "reason"
    And I enter "20" as value, "no" for incorporation, "no" for deactivation, and "yes" for proof marks
    And I click on "Back to application overview"
    And I click on "End use details"
    And I enter "end use details" for the intended end use
    And I select "no" to informed by ECJU to apply
    And I select "no" to informed by ECJU about WMD use
    And I select "no" to suspected WMD use
    And I select "no" to products received under transfer licence from the EU
    And I click save and continue
    And I click on "Provide product location and journey"
    And I select "Great Britain" to where products begin export journey
    And I select "yes" to permanently exported
    And I select "yes" to shipping air waybill or lading
    And I select "directly to the end-user" to who products are going
    And I click on "Submit"
    And I click on "End user"
    And I select "no" to reusing an existing party
    And I select "commercial organisation" as the type of end user
    And I enter the "Joe Bloggs" as end user name
    And I click continue
    And I enter "123 Main Street" and "France" for end user address
    And I enter "Joe Bloggs" for signatory name
    And I select no and enter "reason" for end user document
    And I click on "Submit"
    And I submit the application
    Then my answers are played back to me
    And I see "Standard Individual Export Licence" as the Licence
    And I see "Standard Licence" as the type
    And I see "application1" as reference name
    And I see "No" as informed to apply
    And I see "Great Britain" as product journey origin
    And I see "Yes" as product permanently exported
    And I see "Yes" as way bill
    And I see "Direct to end user" as who are the products going to
    And I see "name" as name
    And I see "N/A" as part number
    And I see "Yes" as controlled
    And I see "ML1a" as control list entry
    And I see "No" as incorporated
    And I see "4 items" as quantity
    And I see "£20.00" as value
    And I see "end use details" as intended end use
    And I see "No" for informed to apply
    And I see "No" for informed WMD
    And I see "No" for suspect WMD
    And I see "No" for EU transfer
    And I see "Joe Bloggs" for end user name
    And I see "Commercial Organisation" for type
    And I see "123 Main Street, France" as address
    And I see "N/A" as website
    And I see "Joe Bloggs" as signatory
    And I see "No, I do not have an end-user undertaking or stockist undertaking" for end user document
    And I see "reason" for the explanation
    And I see "No information added to this section." for "Consignee"
    And I see "No information added to this section." for "Third parties"
    And I see "No information added to this section." for "Supporting documents"
    And I see "No information added to this section." for Notes
    When I click continue
    And I agree to the declaration
    Then application is submitted
    When I go to exporter homepage
    Then I see a banner reminding me to add serial numbers
    When I click on "Add serial number"
    And I click on "Add serial numbers"
    And I input "1234" as serial numbers for items "1,2,3" and press submit
    When I go to exporter homepage
    Then I see a banner reminding me to add serial numbers
    When I click on "Add serial number"
    And I click on "Add serial numbers"
    Then I see serial numbers for items "1,2,3" as "1234"
    When I input "1234" as serial numbers for items "4" and press submit
    And I go to exporter homepage
    Then I don't see a banner reminding me to add serial numbers


  @skip @legacy
  Scenario: Apply for a licence to draft and delete
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    Then I see the application overview
    When I delete the application

  @skip @legacy
  Scenario: Submit standard application permanent
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    And I click on the "location" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I click on the "end_use_details" section
    And I provide details of the intended end use of the products
    And I answer "Yes" for informed by ECJU to apply
    And I answer "No" for informed by ECJU about WMD use
    And I answer "Yes" for suspected WMD use
    And I answer "Yes" for products received under transfer licence from the EU
    And I answer "No" for compliance with the terms of export from the EU
    And I save and continue on the summary page
    And I click on the "route_of_goods" section
    And I answer "Yes" for shipping air waybill or lading
    And I click continue
    And I click on the "goods" section
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on the "end_user" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I click on the "consignee" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I click on the "notes" section
    And I add a note to the draft application
    And I submit the application
    And I click continue
    And I agree to the declaration
    Then application is submitted
    When I go to exporter homepage
    And I click on applications
    Then I see submitted application

  @skip @legacy
  Scenario: Submit standard application with external locations and ultimate end users
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I add an incorporated good to the application
    Then the good is added to the application
    When I click on the "ultimate-end-users" section
    And I click on the add button
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    When I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    And "Delete" link is present
    When I click on the add button
    And I add a party of sub_type: "commercial", name: "Mr Jones", website: " ", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    And I remove an ultimate end user so there is one less
    Then there is only one ultimate end user
    When I click on the "location" section
    And I select "external" for where my goods are located
    And I select "new" for whether or not I want a new or existing location to be added
    And I fill in new external location form with name: "32 Lime Street", address: "London" and country: "Ukraine" and continue
    And I click on add new address
    And I fill in new external location form with name: "place", address: "1 Paris Road" and country: "Ukraine" and continue
    Then I see "2" locations
    When I click on preexisting locations
    And I select the location at position "2" in external locations list and continue
    And I click the back link
    When I click on the "end_user" section
    And I add a party of sub_type: "commercial", name: "Mr Jones", website: " ", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I click on the "end_use_details" section
    And I provide details of the intended end use of the products
    And I answer "No" for informed by ECJU to apply
    And I answer "Yes" for informed by ECJU about WMD use
    And I answer "No" for suspected WMD use
    And I answer "Yes" for products received under transfer licence from the EU
    And I answer "No" for compliance with the terms of export from the EU
    And I save and continue on the summary page
    And I click on the "route_of_goods" section
    And I answer "No" for shipping air waybill or lading
    And I click continue
    And I click on the "consignee" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I submit the application
    And I click continue
    And I agree to the declaration
    When I go to exporter homepage
    And I click on applications
    Then I see submitted application

  @skip @legacy
  Scenario: Submit standard application with external locations and ultimate end users and copy party
    Given I go to exporter homepage and choose Test Org
    And I create a draft
    And I seed an end user for the draft
    When I create a standard application of a "permanent" export type
    And I click on the "end_user" section
    And I select that I want to copy an existing party
    When I filter for my previously created end user
    Then I can select the existing party in the table
    When I click copy party
    And I click continue
    Then I see the party name is already filled in
    When I click continue
    Then I see the party website is already filled in
    When I click continue
    Then I see the party address and country is already filled in
    When I click continue
    And I skip uploading a document

  @skip @legacy
  Scenario: Submit a standard individual transhipment application
    Given I go to exporter homepage and choose Test Org
    When I create a standard individual transhipment application
    And I click on the "location" section
    And I select "external" for where my goods are located
    And I select "new" for whether or not I want a new or existing location to be added
    And I fill in new external location form with name: "32 Lime Street", address: "London" and country: "Ukraine" and continue
    And I click the back link
    And I click on the "end_use_details" section
    And I provide details of the intended end use of the products
    And I answer "Yes" for informed by ECJU to apply
    And I answer "No" for informed by ECJU about WMD use
    And I answer "Yes" for suspected WMD use
    And I answer "No" for products received under transfer licence from the EU
    And I save and continue on the summary page
    And I click on the "route_of_goods" section
    And I answer "Yes" for shipping air waybill or lading
    And I click continue
    And I click on the "goods" section
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on the "end_user" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I click on the "consignee" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I click on the "notes" section
    And I add a note to the draft application
    And I submit the application
    And I click continue
    And I agree to the declaration
    Then application is submitted
    When I go to exporter homepage
    And I click on applications
    Then I see submitted application

  @skip @legacy
  Scenario: Submit standard application temporary
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "temporary" export type
    And I click on the "location" section
    And I select "organisation" for where my goods are located
    And I select the site at position "1"
    And I click continue
    And I click the back link
    And I click on the "end_use_details" section
    And I provide details of the intended end use of the products
    And I answer "Yes" for informed by ECJU to apply
    And I answer "No" for informed by ECJU about WMD use
    And I answer "Yes" for suspected WMD use
    And I answer "Yes" for products received under transfer licence from the EU
    And I answer "No" for compliance with the terms of export from the EU
    And I save and continue on the summary page
    And I click on the "temporary_export_details" section
    And I provide details of why my export is temporary
    And I answer "No" for whether the products remain under my direct control
    And I enter the date "18", "09", "2030" when the products will return to the UK
    And I save and continue on the summary page
    And I click on the "route_of_goods" section
    And I answer "Yes" for shipping air waybill or lading
    And I click continue
    And I click on the "goods" section
    And I add a non-incorporated good to the application
    Then the good is added to the application
    When I click on the "end_user" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I click on the "consignee" section
    And I add a party of sub_type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    And I upload a file "file_for_doc_upload_test_1.txt"
    Then download link is present
    When I click the back link
    And I click on the "notes" section
    And I add a note to the draft application
    And I submit the application
    And I click continue
    And I agree to the declaration
    Then application is submitted
    When I go to exporter homepage
    And I click on applications
    Then I see submitted application


  @skip @legacy
  Scenario: Apply for a standard individual trade control licence draft
    Given I go to exporter homepage and choose Test Org
    When I create a standard individual trade control draft application
    Then I can see the sections "reference-name, goods, end_use_details, route_of_goods, location, end_user, consignee, third-parties, supporting-documents, notes" are on the task list
    When I click on the "location" section
    And I select "external" for where my goods are located
    And I select "new" for whether or not I want a new or existing location to be added
    And I select a location type of "sea_based"
    And I fill in new external location form with name: "32 Lime Street", address: "London" and no country and continue
    And I click on add new address
    And I select a location type of "land_based"
    And I fill in new external location form with name: "32 Lime Street", address: "London" and country: "Ukraine" and continue
    Then I see "2" locations


  @skip @legacy
  Scenario: Review product details when importing existing product, update description and add it to the application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a product from product list
    And I choose to review the product details of product "1"
    And I see option to add product to application on details page
    And I append "updated" to description and submit
    And I see option to add product to application on details page
    # to ensure that we are back on the same page
    And I add product to application


  @skip @legacy @recent
  Scenario: Add a new Firearm product of type firearms, ammunition, components of ammunition to the application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a new product
    And I select product type "firearm"
    And I specify number of items as "4"
    And I select "Yes" for serial number or other identification markings with details as " "
    And I enter "4" serial numbers as "serial1,serial2,serial3,serial4"
    And I enter good name as "Rifle" description as "new firearm" part number "FR-123-M" controlled "True" control code "ML1a" and graded "no"
    And I enter firearm year of manufacture as "2020"
    And I select firearm replica status as "Yes" with description "More details about the replica"
    And I enter calibre as "0.22"
    And I select "No" to registered firearms dealer question
    And I specify firearms act sections apply as "Yes"
    And I select firearms act section "2"
    And I upload firearms certificate file "file_for_doc_upload_test_1.txt"
    And I enter certificate number as "FR2468/1234/1" with expiry date "12-10-2030"
    And I see summary screen for "Firearms" product with name "Rifle" and "continue"
    And I select "Yes" to document available question
    And I select "No" to document is above official sensitive question
    And I upload file "file_for_doc_upload_test_1.txt" with description "File uploaded for firearms product."
    And I enter product details with value "20,000" and deactivated "No" and Save
    Then the product with name "Rifle" is added to the application


  @skip @legacy @recent
  Scenario: Add a new Firearm product of type firearms, ammunition, components of ammunition to the application that is not covered by Firearms Act
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a new product
    And I select product type "component_for_ammunition"
    And I specify number of items as "3"
    And I select "Yes" for serial number or other identification markings with details as " "
    And I enter "3" serial numbers as "serial1,serial2,serial3"
    And I enter good name as "Rifle" description as "new firearm" part number "FR-123-M" controlled "True" control code "ML1a" and graded "no"
    And I enter calibre as "0.22"
    And I select "No" to registered firearms dealer question
    And I specify firearms act sections apply as "Yes"
    And I select firearms act section "2"
    And I upload firearms certificate file "file_for_doc_upload_test_1.txt"
    And I enter certificate number as "FR2468/1234/1" with expiry date "12-10-2030"
    And I see summary screen for "Components for ammunition" product with name "Rifle" and "continue"
    And I select "Yes" to document available question
    And I select "No" to document is above official sensitive question
    And I upload file "file_for_doc_upload_test_1.txt" with description "File uploaded for firearms product."
    And I enter product details with value "20,000" and deactivated "No" and Save
    Then the product with name "Rifle" is added to the application


  @skip @legacy @recent
  Scenario: Add a new Firearm product of type firearms accesory to the application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a new product
    And I select product type "firearm_accessory"
    And I enter good name as "firearm accessory" description as "firearm accessory" part number "FR-123-ACC" controlled "True" control code "ML1a" and graded "no"
    And I specify military use details as "yes_designed"
    And I specify component details as "yes_designed"
    And I specify product employs information security features as "Yes"
    And I see summary screen for "Accessory of a firearm" product with name "firearm accessory" and "continue"
    And I select "Yes" to document available question
    And I select "No" to document is above official sensitive question
    And I upload file "file_for_doc_upload_test_1.txt" with description "File uploaded for firearms product."
    And I enter product details with unit of measurement "Number of articles", quantity "9", value "25,000" and deactivated "No" and Save
    Then the product with name "firearm accessory" is added to the application


  @skip @legacy @recent
  Scenario: Add a new Software relating to a Firearm product to the application
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a new product
    And I select product type "software_for_firearm"
    And I enter good name as "Firearms software" description as "Test software for firearms" part number "FR-123-ACC" controlled "True" control code "ML1a" and graded "no"
    And I specify the "software" product purpose as "For product diagnostics"
    And I specify military use details as "yes_designed"
    And I specify product employs information security features as "Yes"
    And I see summary screen for "Software relating to a firearm" product with name "Firearms software" and "continue"
    And I select "No" to document available question
    And I enter product details with unit of measurement "Number of articles", quantity "25", value "50,000" and deactivated "No" and Save
    Then the product with name "Firearms software" is added to the application


  @skip @legacy @recent
  Scenario: Add a new Firearm product and check if we can edit fields from summary screen
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a new product
    And I select product type "firearm"
    And I specify number of items as "3"
    And I select "Yes" for serial number or other identification markings with details as "serial number FR8654-Z"
    And I enter "3" serial numbers as "serial1,serial2,serial3"
    And I enter good name as "Rifle" description as "new firearm" part number "FR-123-M" controlled "True" control code "ML1a" and graded "no"
    And I enter firearm year of manufacture as "2020"
    And I select firearm replica status as "No" with description "not required"
    And I enter calibre as "0.22"
    And I select "No" to registered firearms dealer question
    And I specify firearms act sections apply as "Yes"
    And I select firearms act section "1"
    And I upload firearms certificate file "file_for_doc_upload_test_1.txt"
    And I enter certificate number as "FR2468/1234/1" with expiry date "12-12-2025"
    And I see summary screen for "Firearms" product with name "Rifle" and "review"
    And I can edit good "Name" as "Powerful Rifle"
    And I can edit good "Description" as "updated firearm description"
    And I can edit good "Part number" as "PN-ABC/123"
    And I can edit good "Year of manufacture" as "2020"
    And I can edit good "Calibre" as "0.45"


  @skip @legacy @recent
  Scenario: Add a new Firearm accessory and check if we can edit fields from summary screen
    Given I go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a new product
    And I select product type "firearm_accessory"
    And I enter good name as "firearm accessory" description as "firearm accessory" part number "FR-123-ACC" controlled "True" control code "ML1a" and graded "no"
    And I specify military use details as "yes_designed"
    And I specify component details as "yes_designed"
    And I specify product employs information security features as "Yes"
    And I see summary screen for "Accessory of a firearm" product with name "firearm accessory" and "review"
    And I can edit good "Name" as "Updated firearm accessory"
    And I can edit good "Description" as "updated firearm accessory description"
    And I can edit good "Part number" as "ACC-123/Y"
    And I can edit good "Military use" as "yes_modified"
    And I can edit good "Information security features" as "No"
