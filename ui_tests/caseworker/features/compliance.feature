@all @internal
Feature: I want to generate and view compliance cases on approval and proviso of OIEL, OICL and specific SIEL applications

  Background: I am setting up a compliance site case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    And all flags are removed
    And the status is set to "submitted"
    And I "approve" the open application good and country at all advice levels
    And A template exists for the appropriate decision
    When I go to the final advice page by url
    And I finalise the advice
    And I approve the good country combination
    And I click continue on the approve open licence page
    And I generate a document for the decision
    And I select the template previously created
    And I click continue
    And I click continue
    And I click continue
    And I go to application previously created
    Then The licence information is in the second audit

  @skip @legacy
  Scenario: Create compliance case
    When I go to the compliance case created
    And I click on the licences tab
    And I show filters
    And I search for the finalised licence
    And I apply filters
    Then I see my previously created licence
    When I go to the compliance case created
    And I click add a visit report
    Then I am on a compliance visit case
    When I add I visit report details 'First visit', '2020-05-12', 'Lower risk', and '5'
    Then I see the visit report details in details and the banner
    When I add person present 'John Smith' who works as 'Product Manager'
    Then I see the people present
    When I add overview details of 'The overview'
    Then I see overview details
    When I add inspection details of 'The inspection'
    Then I see inspection details
    When I add Compliance with licences details 'Compliance with licence overview' and 'Highest risk'
    Then I see Compliance with licences details
    When I add knowledge of key individuals details 'knowledge of key individuals' and 'Medium risk'
    Then I see knowledge of key individuals details
    When I add knowledge of controlled product details 'knowledge of controlled products' and 'Higher risk'
    Then I see knowledge of controlled product details
    When I go to the ECJU queries tab
    Then I see different ecju query buttons
