export const post = async (uri, fixture, headers) => {
  let data
  await new Promise((generateData) => {
    cy.request({
      method: 'POST',
      url: `${Cypress.env('api_url')}${uri}`,
      json: true,
      body: fixture,
      headers: headers || {},
    }).then(async response => {
      data = response.body
      generateData(data)
    })
  })
  return data
}
