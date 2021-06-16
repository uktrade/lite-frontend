Feature: I want to indicate the standard licence I want
  As a logged in exporter
  I want to submit SIEL applications involving firearms products

  Scenario: Add a new Firearm product of type firearms, ammunition, components of ammunition to the application
    Given I signin and go to exporter homepage and choose Test Org
    When I create a standard application of a "permanent" export type
    When I click on the "goods" section
    And I choose to add a new product
    And I select product category "firearms"
    And I select product type "firearm"
    And I select sporting shotgun status as "Yes"
    And I specify number of items as "4"
    And I select "Yes" for serial number or other identification markings with details as " "
    And I enter "4" serial numbers as "serial1,serial2,serial3,serial4"
    And I enter good name as "Rifle" description as "new firearm" part number "FR-123-M" controlled "True" control code "PL9002" and graded "no"
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
    And I logout
