@all @tau
Feature: I want to check application with precedents

  Scenario: Using previous assessment to assess a good on application
    Given I sign in to SSO or am signed into SSO
    Given I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And I set the case status to "Submitted"
    # LR
    When I switch to "Licensing Reception" with queue "Licensing Reception SIEL applications" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Enforcement Unit Cases to Review, Technical Assessment Unit SIELs to Review"
    # EU
    When I switch to "Enforcement Unit" with queue "Enforcement Unit Cases to Review" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Technical Assessment Unit SIELs to Review"
    And I see the case is not assigned to queues "Enforcement Unit Cases to Review"
    # TAU
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Technical Assessment Unit SIELs to Review"
    And I go to my case list
    Then I see previously created application
    When I click on the application previously created
    And I assign myself to the case
    Then I click on Product assessment
    And I select all goods
    And I select the CLE "ML1a"
    And I select "components for" / "microwave components" as report summary prefix / subject and regime to none and submit
    When I click move case forward
    Then I don't see previously created application
    # Make next application with asssessed goods
    When I go to my profile page
    And I change my team to "Admin" and default queue to "All cases"
    Given I go to internal homepage
    When I create an application with re-used "Rifle" goods
    Then I see previously created application
    # LR
    When I switch to "Licensing Reception" with queue "Licensing Reception SIEL applications" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Enforcement Unit Cases to Review, Technical Assessment Unit SIELs to Review"
    # EU
    When I switch to "Enforcement Unit" with queue "Enforcement Unit Cases to Review" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Technical Assessment Unit SIELs to Review"
    And I see the case is not assigned to queues "Enforcement Unit Cases to Review"
    # TAU
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Technical Assessment Unit SIELs to Review"
    And I go to my case list
    Then I see previously created application
    When I click on the application previously created
    And I assign myself to the case
    # Scenario starts
    Then I click on Product assessment
    Then I check if the URL contains "previous-assessments"
    And I deselect all checkboxes
    Then I select good called "Rifle" and approve and continue
    Then I assert if "Rifle" has been assessed

    Examples:
      | name    | product        | part_number | clc_rating  | end_user_name | end_user_address| consignee_name    | consignee_address | country | end_use                  |
      | Test12  | Rifle, Shotgun | PN-ABC-123  | PL9002      | Joe bloggs    | 123 Main street | Josephine Bloggs  | 123 Main Street   | BL      | Research and development |

  Scenario: Multiple edits for asssessed goods
    Given I sign in to SSO or am signed into SSO
    Given I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>
    And I set the case status to "Submitted"
    # LR
    When I switch to "Licensing Reception" with queue "Licensing Reception SIEL applications" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Enforcement Unit Cases to Review, Technical Assessment Unit SIELs to Review"
    # EU
    When I switch to "Enforcement Unit" with queue "Enforcement Unit Cases to Review" and I submit the case
    Then I see the case status is now "Initial checks"
    And I see the case is assigned to queues "Technical Assessment Unit SIELs to Review"
    And I see the case is not assigned to queues "Enforcement Unit Cases to Review"
    # TAU
    When I go to my profile page
    And I change my team to "Technical Assessment Unit" and default queue to "Technical Assessment Unit SIELs to Review"
    And I go to my case list
    Then I see previously created application
    When I click on the application previously created
    And I assign myself to the case
    Then I click on Product assessment
    And I select all goods
    And I select the CLE "ML1a"
    And I select "components for" / "microwave components" as report summary prefix / subject and regime to none and submit
    # Scenario starts
    Then I click on Product assessment
    And I click on "Edit assessments" button
    Then I edit the fields and checks if they were updated

    Examples:
      | name    | product        | part_number | clc_rating  | end_user_name | end_user_address| consignee_name    | consignee_address | country | end_use                  |
      | Test34  | Rifle, Shotgun | PN-ABC-123  | PL9002      | Joe bloggs    | 123 Main street | Josephine Bloggs  | 123 Main Street   | BL      | Research and development |
