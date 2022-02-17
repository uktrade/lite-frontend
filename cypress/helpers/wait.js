import { exporter } from '../fixtures/headers'
import { get } from './request'

const waitForDocumentToBeScanned = async (uri, token, orgId, multipleDocuments = true, counter = 0, timeout = 5000) => { 
  if (counter > timeout) {
    return
  }
  const response = await get(uri, exporter(token, orgId))
  if (multipleDocuments) {
    if (response.documents[0].safe == true) {
      return
    }
  } else {
    if (response.document.safe == true) {
      return
    }
  }
  counter += 100
  cy.wait(counter)
  waitForDocumentToBeScanned(uri, token, orgId, multipleDocuments, counter)
}

module.exports = { waitForDocumentToBeScanned }
