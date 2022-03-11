import '@testing-library/cypress/add-commands'

Cypress.Commands.add('login', () => {
  cy.request(Cypress.env('sso_url')).then((getResponse) => {
    const loginCsrfCookie = getResponse.headers['set-cookie'][0]
    const csrfToken = loginCsrfCookie.match("csrftoken=(.*); expires")
    const options = {
      method: 'POST',
      url: Cypress.env('sso_url'),
      form: true,
      body: {
        username: Cypress.env('sso_user'),
        password: Cypress.env('sso_password'),
        csrfmiddlewaretoken: csrfToken[1],
      },
      headers: {
        referer: Cypress.env('sso_url'),
      }
    }
    cy.request(options)
  })
})
