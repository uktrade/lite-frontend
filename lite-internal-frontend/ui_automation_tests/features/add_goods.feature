@goods @all
Feature: I want to add a clc-case good to the goods list
    As a logged in exporter
    I want to add a clc-case good to the goods list
    So that I can ensure the good is listed in my cases

    @LT-1006_add_clc_query_good
    Scenario: Add "I don't know" good
        Given I go to exporter homepage
        When I login to exporter homepage with username "test@mail.com" and "password"
        And I click on goods link
        When I click add a good button
        And I add a good a clc-case good with description "Description"
        When I see clc-good in goods list
        Given I go to internal homepage
        Then I see the clc-case previously created
