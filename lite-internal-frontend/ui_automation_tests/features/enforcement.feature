@all @internal @enforcement
Feature: I want to export and import XML for enforcement checking
  As a logged in government user
  I want to download the entities for all application cases on a queue in XML format
  So that I can upload it to an entity checking system to look for a match

  @LT_1309_enforcement_check_export_xml @regression
  Scenario: Export all cases on a work queue for an enforcement check
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And a queue has been created
    And case has been moved to new Queue
    When I go to my work queue
    Then I should see my case in the cases list
    When I click export enforcement xml
    Then the enforcement check is audited
