import helper from '../../helpers'
import fixtures from '../../fixtures'

describe('Application', () => {
  // it('login', () => {
  //   cy.login()
  // })

  context('newly created application', () => {
    let organisationId
    let userToken
    let exportUserToken
    let applicationId
    let goodId
    let endUserId

    before(async () => {
      // Retrieve user token
      const authResponse = await helper.post(
        'gov-users/authenticate/',
        fixtures.authUser(Cypress.env('sso_user'))
      )
      userToken = await authResponse.token

      // Retrieve export user token
      const exportAuthResponse = await helper.post(
        'users/authenticate/',
        fixtures.exportAuthUser(Cypress.env('export_sso_user'))
      )
      exportUserToken = await exportAuthResponse.token

      // Create organisation
      const organisationResponse = await helper.post(
        'organisations/',
        fixtures.organisation(),
        fixtures.headers.caseworker(userToken),
      )
      organisationId = organisationResponse.id

      // Update organsation status to Active
      await helper.put(
        `organisations/${organisationId}/status/`,
        { status: 'active'},
        fixtures.headers.caseworker(userToken),
      )

      // Add user to organisation caseworker
      await helper.post(
        `organisations/${organisationId}/users/`,
        fixtures.userToOrg(Cypress.env('sso_user')),
        fixtures.headers.caseworker(userToken),
      )

      // Create an application
      const applicationResponse = await helper.post(
        'applications/',
        fixtures.applicaton.create,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )
      applicationId = applicationResponse.id
      
      // Create goods
      const goodsResponse = await helper.post(
        'goods/',
        fixtures.goods,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )
      goodId = goodsResponse.good.id

      // Create good document
      await helper.post(
        `goods/${goodId}/documents/`,
        [fixtures.document('goods document', 'some goods document')],
        fixtures.headers.exporter(exportUserToken, organisationId)
      )

      // Add goods to application
      await helper.post(
        `applications/${applicationId}/goods/`,
        {...fixtures.goods, good_id: goodId},
        fixtures.headers.exporter(exportUserToken, organisationId)
      )
      
      // // Add external location to application
      // const addLocationToDraftResponse = await helper.post(
      //   `applications/${applicationId}/sites/`,
      //   { sites: ['f2ce553e-c1df-4650-86ac-c89028a1459a'] },
      //   fixtures.headers.exporter(exportUserToken, organisationId)
      // )

      // Add end user to application
      const addEndUserToDraftResponse = await helper.post(
        `applications/${applicationId}/parties/`,
        fixtures.parties.endUser,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )
      endUserId = addEndUserToDraftResponse.end_user.id
      
      // Add document to end user
      await helper.post(
        `applications/${applicationId}/parties/${endUserId}/document/`,
        fixtures.document('party document', 'some party document'),
        fixtures.headers.exporter(exportUserToken, organisationId)
      )

      // Add ultimate end user to application
      await helper.post(
        `applications/${applicationId}/parties/`,
        fixtures.parties.ultimateEndUser,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )
      
      // Add consignee to application
      await helper.post(
        `applications/${applicationId}/parties/`,
        fixtures.parties.consignee,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )

      // Add Third Party to application
      await helper.post(
        `applications/${applicationId}/parties/`,
        fixtures.parties.thirdParty,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )

      // Add end use details to application
      await helper.put(
        `applications/${applicationId}/end-use-details/`,
        fixtures.endUseDetails,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )

      // Add route of goods to application
      await helper.put(
        `applications/${applicationId}/route-of-goods/`,
        fixtures.routeOfGoods,
        fixtures.headers.exporter(exportUserToken, organisationId)
      )

      // Submit an application
      const submitApplicationResponse = await helper.put(
        `applications/${applicationId}/submit/`,
        fixtures.applicaton.submit,
        fixtures.headers.exporter(exportUserToken, organisationId)
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
