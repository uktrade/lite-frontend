@exporter @set_up  @all @goods
Feature: Set up goods
As a...

    Scenario: Set up goods
        Given I go to exporter homepage
        When I login to exporter homepage with username "test@mail.com" and "password"
        And I click on goods link
        When I click add a good button
        And I add a good or good type with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
        Then I see good in goods list
        When I click add a good button
        When I add a good or good type with description "Good T2" controlled "Yes" control code "2345" incorporated "Yes" and part number "3456"
        Then I see good in goods list
        When I click add a good button
        When I add a good or good type with description "Good T3" controlled "Yes" control code "535" incorporated "Yes" and part number "111"
        Then I see good in goods list

    Scenario: Edit and delete good
        Given I go to exporter homepage
        When I login to exporter homepage with username "test@mail.com" and "password"
        And I click on goods link
        When I click add a good button
        And I add a good or good type with description "aa" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
        And I edit a good to description "edited" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
        Then I see my edited good in the goods list
        When I delete my good
        Then my good is no longer in the goods list

    Scenario: Rollback
        Given I go to exporter homepage
        When I login to exporter homepage with username "test@mail.com" and "password"
        And I click on goods link
        Then Rollback goods
