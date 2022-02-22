const request = async (uri, fixture, headers, method) => {
  let data
  await new Promise((generateData) => {
    cy.request({
      method,
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

exports.post = async (uri, fixture, headers) => {
  return request(uri, fixture, headers, 'POST')
}

exports.put = async (uri, fixture, headers) => {
  return request(uri, fixture, headers, 'PUT')
}

exports.get = async (uri, headers) => {
  return request(uri, {}, headers, 'GET')
}
