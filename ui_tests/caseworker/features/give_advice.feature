@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @fcdo_approve_advice
  Scenario: FCDO to approve advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I assign the case to "FCDO Cases to Review" queue
    And I go to my profile page
    And I change my team to "FCDO" and default queue to "FCDO Cases to Review"
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
    And I change my team to "FCDO" and default queue to "FCDO Counter-signing"
    And I go to my case list
    Then I should see my case in the cases list
    # Check the recommendation is listed
    When I click the application previously created
    And I click the recommendations and decision tab
    And I expand the details for "FCDO has approved"
    Then I should see my recommendation for "Great Britain, Ukraine" with "Hello World"

  @mod_approve_advice
  Scenario: MOD approve advice journey
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
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
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
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
    When I click "Review and combine"
    And I enter "overall reason" as the overall reason
    And I enter "licence condition1" as the licence condition
    And I click submit recommendation
    Then I see "overall reason" as the overall reason
    And I see "licence condition1" as the licence condition
    When I click move case forward
    Then I don't see previously created application


  @mod_edit_advice
  Scenario: MOD edit advice journey
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
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
    When I click "Edit recommendation"
    And I enter "reason for approving1" as the reasons for approving
    And I enter "licence condition1" as the licence condition
    And I enter "instruction for exporter1" as the instructions for the exporter
    And I enter "reporting footnote1" as the reporting footnote
    And I click submit recommendation
    Then I see "reason for approving1" as the reasons for approving
    And I see "licence condition1" as the licence condition
    And I see "instruction for exporter1" as the instructions for the exporter
    And I see "reporting footnote1" as the reporting footnote


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
    And I see "licence condition" as the licence condition
    And I see "instruction for exporter" as the instructions for the exporter
    And I see "reporting footnote" as the reporting footnote
    When I click "Clear recommendation"
    And I click confirm
    Then I am asked what my recommendation is
    When I click back
    Then I see there are no recommendations from "MOD-WECA"


  @mod_refuse_advice
  Scenario: MOD refuse advice journey
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
    And I click refuse all
    And I click continue
    And I select refusal criteria "1a, 1b, 1c, 1d, 1e, 1f"
    And I enter "reason for this refusal" as the reasons for refusal
    And I click submit recommendation
    Then I see "reason for this refusal" as the reasons for refusal
    # The following step will implicitly navigate through the "All cases" queue
    When I go to application previously created
    And I click the recommendations and decision tab
    And I expand the details for "MOD-WECA has refused"
    Then I see "reason for this refusal" as the reasons for refusal
    And I see "1a, 1b, 1c, 1d, 1e, 1f" as the refusal criteria


  @lu_consolidate_advice
  Scenario: LU consolidate advice journey
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I prepare the application for final review
    When I go to my profile page
    And I change my team to "Licensing Unit" and default queue to "Licensing Unit Post-circulation Cases to Finalise"
    And I go to my case list
    And I click the application previously created
    And I click the recommendations and decision tab
    And I click "Review and combine"
    And I enter "reason for approving" as the reasons for approving
    And I enter "licence condition" as the licence condition
    And I click submit recommendation
    Then I see "reason for approving" as the reasons for approving
    And I see "licence condition" as the licence condition
    When I click "Finalise case"
    And I click save
    And I click "Generate"
    And I select the template "SIEL template"
    And I click continue
    And I click preview
    Then I see the licence number on the SIEL licence preview
    And I see that "16. Control list no" is "ML1a" on the SIEL licence preview
    When I click continue
    And I click save and publish to exporter
    Then I see the case status is now "Finalised"
    And I see the case is not assigned to any queues
