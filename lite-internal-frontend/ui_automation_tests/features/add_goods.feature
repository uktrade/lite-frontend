@goods @all
Feature: I want to add a clc-case good to the goods list
    As a logged in exporter
    I want to add a clc-case good to the goods list
    So that I can ensure the good is listed in my cases

    @LT-1006_add_clc_query_good
    Scenario: Add "I don't know" good
        Given I go to exporter homepage
        When I login to exporter homepage with username "trinity@unicorns.com" and "12345678900"
        And I click on goods link
        And I click add a good button
        And I add a good a clc-case good with description "MPG 2.9"
        And I see clc-good in goods list
        And I go to internal homepage and sign in
        Then I see the clc-case previously created
