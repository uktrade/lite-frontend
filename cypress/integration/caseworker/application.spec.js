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
      // Create organisation
      const organisationResponse = await helper.post('organisations/', fixtures.organisation())
      organisationId = organisationResponse.id

      // Retrieve exporter user token
      const authResponse = await helper.post('gov-users/authenticate/', fixtures.authUser(Cypress.env('sso_user')))
      userToken = await authResponse.token

      // Update organsation status to Active
      await helper.put(
        `organisations/${organisationId}/status/`,
        { status: 'Active '},
        fixtures.exporterHeader(userToken, organisationId)
      )

      // Add user to organisation
      await helper.post(
        `organisations/${organisationId}/users/`,
        fixtures.userToOrg(),
        fixtures.exporterHeader(userToken, organisationId)
      )
      
      // Create an application
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
