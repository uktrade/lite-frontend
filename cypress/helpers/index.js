module.exports = {
  post: require('./request').post,
  put: require('./request').put,
  get: require('./request').get,
  waitForDocumentToBeScanned: require('./wait').waitForDocumentToBeScanned,
}
