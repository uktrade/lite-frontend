export const post = async (uri, fixture) => {
  fixture.name = `Org-2022${Math.floor(Math.random() * 10000000000000)}`

  return cy.request({
    method: 'POST',
    url: `${Cypress.env('api_url')}${uri}`,
    json: true,
    body: fixture,
  })
}
