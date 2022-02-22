import { createApplication } from '../../api/createApplication'

describe('Login', () => {
  it('login', () => {
    cy.login()
  })

  describe('Application', () => {
    let response

    before(async () => {
      // Change domain
      cy.visit('/')
      response = await createApplication()
    })

    it('should submit a case for a newly created application', () => {
      cy.visit(`/queues/${response.defaultQueue}/cases/${response.applicationId}/`)
      cy.get('#heading-reference-code')
        .should('contain', response.submittedApplication.reference_code)
    })
  })
})
