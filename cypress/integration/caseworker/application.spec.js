import helper from '../../helpers'
import fixtures from '../../fixtures'

describe('Application', () => {
  // it('login', () => {
  //   cy.login()
  // })

  context('newly created application', () => {
    let organisationId
    let userToken

    before(async () => {
      const organisationResponse = await helper.post('organisations/', fixtures.organisation())
      organisationId = organisationResponse.id
      const authResponse = await helper.post('gov-users/authenticate/', fixtures.authUser(Cypress.env('sso_user')))
      userToken = await authResponse.token
      const applicationResponse = await helper.post(
        'applications/',
        fixtures.applicaton,
        fixtures.exporterHeader(userToken, organisationId)
      )
      cy.pause()
    })

    beforeEach(() => {
      cy.visit('/')
    })

    it('should approve a case', () => {
      cy.visit('/application/')
    })
  })
})
