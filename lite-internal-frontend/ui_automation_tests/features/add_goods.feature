@goods @all
Feature: I want to add a clc-case good to the goods list
    As a logged in exporter
    I want to add a clc-case good to the goods list
    So that I can ensure the good is listed in my cases

    @LT_1006_add_clc_query_good
    Scenario: Add "I don't know" good
        Given I go to internal homepage
        Then I see the clc-case previously created

    @LT_1584_click_on_good
    Scenario: Click on good
        Given I create application or application has been previously created
        And I go to internal homepage
        When I go to application previously created
        And I click on good
        Then I see good information