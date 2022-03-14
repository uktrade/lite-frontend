@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @fcdo_approve_case
  Scenario: FCDO to approve a case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign the case to "FCO Cases to Review" queue
    And I go to my profile page
    And I change my team to "FCO" and default queue to "FCO Cases to Review"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I select countries "GB, UA"
    And I enter "Hello World" as the reasons for approving
    And I click submit recommendation
    Then I should see my recommendation for "Great Britain, Ukraine" with "Hello World"
    When I click move case forward
    Then I don't see previously created application
    # Check the case has moved to the correct queue
    When I go to my profile page
    And I change my team to "FCO" and default queue to "FCO Counter-signing"
    And I go to my case list
    Then I should see my case in the cases list
    # Check the recommendation is listed
    When I click the application previously created
    And I click the recommendations and decision tab
    And I expand the details for "FCO has approved"
    Then I should see my recommendation for "Great Britain, Ukraine" with "Hello World"


  @mod_advice
  Scenario: MOD advice journey
    ##### MOD to circulate a case #####
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign the case to "Circulate to sub-advisers" queue
    And I go to my profile page
    And I change my team to "MOD-ECJU" and default queue to "Circulate to sub-advisers"
    And I go to my case list
    And I click the application previously created
    And I assign the case to "MOD-WECA Cases to Review" queue
    And I click I'm done
    And I click submit
    Then I don't see previously created application

    ##### Sub-advisor to give advice #####
    When I go to my profile page
    And I change my team to "MOD-WECA" and default queue to "MOD-WECA Cases to Review"
    And I go to my case list
    Then I should see my case in the cases list
    When I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I enter "reason for approving" as the reasons for approving
    And I enter "licence condition" as the licence condition
    And I enter "instruction for exporter" as the instructions for the exporter
    And I enter "reporting footnote" as the reporting footnote
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    Then I see "licence condition" as the licence condition
    Then I see "instruction for exporter" as the instructions for the exporter
    Then I see "reporting footnote" as the reporting footnote
    When I click move case forward
    Then I don't see previously created application

    ##### MOD-ECJU to consolidate #####
    When I go to my profile page
    And I change my team to "MOD-ECJU" and default queue to "Review and combine"
    And I go to my case list
    Then I should see my case in the cases list
    When I click the application previously created
    And I click the recommendations and decision tab
    And I expand the details for "MOD-ECJU has approved with licence conditions"
    Then I see "reason for approving" as the reasons for approving
    Then I see "licence condition" as the licence condition
    Then I see "instruction for exporter" as the instructions for the exporter
    Then I see "reporting footnote" as the reporting footnote
    When I click "Review and combine"
    And I enter "overall reason" as the overall reason
    And I enter "licence condition1" as the licence condition
    And I click submit recommendation
    Then I see "overall reason" as the overall reason
    Then I see "licence condition1" as the licence condition
    When I click move case forward
    Then I don't see previously created application


  @mod_clear_advice
  Scenario: MOD clear advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign the case to "MOD-WECA Cases to Review" queue
    And I go to my profile page
    And I change my team to "MOD-WECA" and default queue to "MOD-WECA Cases to Review"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click make recommendation
    And I click approve all
    And I click continue
    And I enter "reason for approving" as the reasons for approving
    And I enter "licence condition" as the licence condition
    And I enter "instruction for exporter" as the instructions for the exporter
    And I enter "reporting footnote" as the reporting footnote
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    Then I see "licence condition" as the licence condition
    Then I see "instruction for exporter" as the instructions for the exporter
    Then I see "reporting footnote" as the reporting footnote
    When I click "Clear recommendation"
    And I click confirm
    Then I am asked what my recommendation is
    When I click "Back"
    Then I see there are no recommendations from "MOD-WECA"
