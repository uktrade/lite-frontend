import { createApplication } from '../../api/createApplication'


describe('Application', () => {
  const counterSignQueue = Cypress.env('fco_counter_sign_queue')
  let response

  before(async () => {
    cy.login()
    cy.visit('/')
    response = await createApplication()
  })

  it('should approve a case in FCDO queue with the correct information', () => {
    cy.visit(`/queues/${response.defaultQueue}/cases/${response.applicationId}/`)
    cy.get('#heading-reference-code')
      .should('contain', response.submittedApplication.reference_code)
    cy.visit(`/queues/${response.defaultQueue}/cases/${response.applicationId}/advice`)
    cy.findByText('Make recommendation').click()
    cy.findByText('Approve all').click()
    cy.findByText('Continue').click()
    cy.get('[type="checkbox"]').check('BE')
    cy.get('[type="checkbox"]').check('UA')
    cy.get('textarea').first().type('FCDO Approval Reason')
    cy.findByText('Submit recommendation').click()
    cy.get('.govuk-main-wrapper')
      .should('contain', 'Approved by Test Lite')
      .should('contain', 'Belgium')
      .should('contain', 'Ukraine')
      .should('contain', 'FCDO Approval Reason')
    cy.findByText('Move case forward').click()

    cy.visit(`/queues/${response.defaultQueue}/?case_reference=${response.submittedApplication.reference_code}`)
    cy.get('#form-cases').should('contain', 'There are no new cases')
  })

  it('should approve a case in FCO Counter-signing queue with the correct information', () => {
    cy.visit('/').then(() => {
      cy.visit(`/queues/${counterSignQueue}/cases/${response.applicationId}/details/`)
    })
    cy.get('#assigned-queues')
      .should('not.contain', 'FCO Cases to Review')
      .should('contain', 'FCO Counter-signing')
    cy.visit(`/queues/${counterSignQueue}/cases/${response.applicationId}/advice/countersign/`)
    cy.get('.govuk-details__text')
      .should('contain', 'Belgium')
      .should('contain', 'Ukraine')
      .should('contain', 'FCDO Approval Reason')

    cy.visit(`/queues/${counterSignQueue}/cases/${response.applicationId}/advice/countersign/`)
    cy.findByText('Review and countersign').click()
    cy.get('textarea').first().type('Countersign Approval Reason')
    cy.findByText('Submit recommendation').click()
    cy.findByText('Countersign Approval Reason').should('exist')
    cy.findByText('FCDO Approval Reason').should('exist')
    cy.findByText('Move case forward').click()

    cy.visit(`/queues/${counterSignQueue}/cases/${response.applicationId}/details/`)
    cy.get('#assigned-queues')
      .should('not.contain', 'FCO Cases to Review')
      .should('not.contain', 'FCO Counter-signing')
      .should('contain', 'MOD Cases to Review')
  })
})
