@all @internal @filter_and_sort
Feature: I want to filter cases on a queue
  As a logged in government user
  I want to filter the cases in the work queue I am viewing
  So that I can easily find the cases I am most interested in

  @skip @legacy
  Scenario: Filter cases
    Given I sign in to SSO or am signed into SSO
    And a queue has been created
    And I create open application or open application has been previously created
    And case has been moved to new Queue
    And I go to internal homepage
    When I show filters
    And I click advanced filters
    Then I can see all advanced filters
    When I filter by case reference
    And I filter by goods related description
    And I filter by organisation name
    When I apply filters
    Then "1" cases are shown
    When I show filters
    Given I create a clc query
    When case has been moved to new Queue
    And I click on new queue in dropdown
    Then "2" cases are shown
    When I show filters
    Then the filters are shown
    When filter status has been changed to "Finalised"
    Then there are no cases shown
    When I show filters
    When I click clear filters
    When I show filters
    When filter case type has been changed to "Goods Query"
    Then "1" cases are shown
    When I show filters
    When filter status has been changed to "CLC review"
    Then "1" cases are shown
    When I show filters
    When I click clear filters
    Then "2" cases are shown
    When I go to application previously created
    And I click change status
    And I select status "Under review" and save
    And I go to the internal homepage
    And I click on new queue in dropdown
    # Application is removed due to case routing rules and change of status
    Then "1" cases are shown
    When I show filters
    And I click filter to show cases with open team ecju queries
    Then "1" cases are shown
