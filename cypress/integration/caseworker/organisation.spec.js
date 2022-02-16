import helper from '../../helpers'
import fixtures from '../../fixtures'

const filterOrganisation = (cy, organisationName) => {
  cy.findByText('Show filters').click()
  cy.get('#search_term').type(organisationName)
  cy.findByText('Apply filters').click()
  cy.findByText(organisationName).click()
}

describe('Organisation', () => {
  it('login', () => {
    cy.login()
  })

  context('newly created organisation', () => {
    let organisation

    before(async function () {
      const response = await helper.post('organisations/', fixtures.organisation())
      organisation = response
    })

    beforeEach(() => {
      cy.visit('/')
    })

    it('should approve an organisation', () => {
      cy.visit('/organisations/')

      cy.findByText('In review').click()
      filterOrganisation(cy, organisation.name)
      cy.findByText('Review').click()

      cy.get('.govuk-summary-list')
        .should('contain', organisation.name)
        .and('contain', organisation.eori_number)
        .and('contain', organisation.sic_number)
        .and('contain', organisation.vat_number)
        .and('contain', organisation.registration_number)
        .and('contain', organisation.type.value)

      cy.get('#status-active').click()
      cy.findByText('Save').click()
      cy.findByText('Active').should('exist')
      cy.findByText(`activated the organisation - '${organisation.name}'.`)
        .should('exist')

      cy.visit('/organisations/')

      cy.findByText('Active').click()
      filterOrganisation(cy, organisation.name)
    })
  })
})
