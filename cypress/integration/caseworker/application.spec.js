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

    it('should approve a case for a newly created application', () => {
      cy.visit(`/queues/${response.defaultQueue}/cases/${response.applicationId}/`)
      cy.get('#heading-reference-code')
        .should('contain', response.submittedApplication.reference_code)
      cy.visit(`/queues/${response.defaultQueue}/cases/${response.applicationId}/advice`)
      cy.findByText('Make recommendation').click()
      cy.findByText('Approve all').click()
      cy.findByText('Continue').click()
      cy.get('[type="checkbox"]').check('BE')
      cy.get('[type="checkbox"]').check('UA')
      cy.get('textarea').first().type('Hello world')
      cy.findByText('Submit recommendation').click()
      cy.get('.govuk-main-wrapper')
        .should('contain', 'Approved by Test Lite')
        .should('contain', 'Belgium')
        .should('contain', 'Ukraine')
        .should('contain', 'Hello world')
      cy.findByText('Move case forward').click()

      cy.visit(`/queues/${response.defaultQueue}/?case_reference=${response.submittedApplication.reference_code}`)
      cy.get('#form-cases').should('contain', 'There are no new cases')
    })

    it('should display case in counter sign queue with the correct information', () => {
      cy.visit('/').then(() => {
        cy.visit(`/queues/${Cypress.env('fco_counter_sign_queue')}/cases/${response.applicationId}/details/`)
      })
      cy.get('#assigned-queues')
        .should('not.contain', 'FCO Cases to Review')
        .should('contain', 'FCO Counter-signing')
      cy.visit(`/queues/${Cypress.env('fco_counter_sign_queue')}/cases/${response.applicationId}/advice/countersign/`)
      cy.get('.govuk-details__text')
        .should('contain', 'Belgium')
        .should('contain', 'Ukraine')
        .should('contain', 'Hello world')
    })
  })
})
