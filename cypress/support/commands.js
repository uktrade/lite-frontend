import '@testing-library/cypress/add-commands'

Cypress.Commands.add('login', () => {
  cy.visit(Cypress.env('sso_url'))
  cy.get('#id_username').type(Cypress.env('sso_user'), { log: false })
  cy.get('#id_password').type(Cypress.env('sso_password'), { log: false })
  cy.findByText('login').click()
  cy.findByText('You have signed in to DIT internal services')
    .should('exist')
})

Cypress.Commands.add('setCsrfTokenCookie', () => {
  cy.setCookie('csrftoken', 'WAzzVOJCY27ZNs6snAEC775y8W1HDXYJq09otCot3PO1KRYrvSbExjV9Cr6QYmFl', {
    domain: "sso.trade.uat.uktrade.io",
    expiry: 1675166092.722795,
    httpOnly: false,
    path: "/",
    sameSite: "lax",
    secure: false,
  })
})

Cypress.Commands.add('createOrganisation', (fixture) => {
  const URI = 'organisations/'
  fixture.name = `Org-2022${Math.floor(Math.random() * 10000000000000)}`
  return cy.request({
    method: 'POST',
    url: `${Cypress.env('api_url')}${URI}`,
    json: true,
    body: fixture,
  })
})
