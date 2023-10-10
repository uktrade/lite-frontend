# Mock SSO

The purpose of mock sso is to give us the ability to swap out the external third party sso services that we use.

Swapping this out is useful when:

  - we are running end-to-end tests and we don't want to rely on external services
  - we want to login as a different user locally
  - we want to develop locally without an internet connection

The two services that we currently integrate with are:

  - DBT SSO - for caseworker
  - GOV.UK One Login - for exporter

Mock sso isn't meant as a direct replica of either of these services, as it skips out functionality that isn't necessary for a user to login to LITE, the intention of this code is to provide the smallest amount of functionality that allows a user to be logged in and for the SSO code to pass.
