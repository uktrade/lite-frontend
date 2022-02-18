import helper from '../helpers'
import fixtures from '../fixtures'

export const createApplication = async () => {
  let organisationId
  let userToken
  let defaultQueue
  let exportUserToken
  let applicationId
  let goodId
  let endUserId
  let siteId
  let submittedApplication

  // Retrieve user token
  const authResponse = await helper.post(
    'gov-users/authenticate/',
    fixtures.authUser(Cypress.env('sso_user'))
  )
  userToken = authResponse.token
  defaultQueue = authResponse.default_queue

  // Retrieve export user token
  const exportAuthResponse = await helper.post(
    'users/authenticate/',
    fixtures.exportAuthUser(Cypress.env('export_sso_user'))
  )
  exportUserToken = exportAuthResponse.token

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

  // Create site for organisation
  const siteResponse = await helper.post(
    `organisations/${organisationId}/sites/`,
    fixtures.site,
    fixtures.headers.caseworker(userToken),
  )
  siteId = siteResponse.site.id

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

  // Add location to application
  await helper.post(
    `applications/${applicationId}/sites/`,
    {'sites': [siteId]},
    fixtures.headers.exporter(exportUserToken, organisationId)
  )

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
  
  // Wait until document has been scanned
  await helper.waitForDocumentToBeScanned(
    `goods/${goodId}/documents/`,
    exportUserToken,
    organisationId,
  )

  // Wait until document has been scanned
  await helper.waitForDocumentToBeScanned(
    `applications/${applicationId}/parties/${endUserId}/document/`,
    exportUserToken,
    organisationId,
    false,
  )

  // Submit an application
  const submittedApplicationResponse = await helper.put(
    `applications/${applicationId}/submit/`,
    fixtures.applicaton.submit,
    fixtures.headers.exporter(exportUserToken, organisationId)
  )
  submittedApplication = submittedApplicationResponse.application

  // Change application status
  await helper.put(
    `applications/${applicationId}/status/`,
    fixtures.applicaton.status('ogd_advice'),
    fixtures.headers.caseworker(userToken),
  )
  
  return { submittedApplication, defaultQueue, applicationId }
}
