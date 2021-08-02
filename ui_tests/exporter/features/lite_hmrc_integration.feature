Feature: I want to know that licence data goes to and comes from HMRC via email

  @an_exporter_test
  Scenario: Check that licence data has gotten to HMRC via email
    Given I set all emails in lite-hmrc to reply-sent
    And I signin and go to exporter homepage and choose Test Org
    And I create a standard application via api
    And I remove the flags
    And I create "approve" final advice
    And I create a licence for my application with "approve" decision document and good decisions
    And I force lite-hmrc to send pending licences now
    Then I confirm a licence has been sent to HMRC
