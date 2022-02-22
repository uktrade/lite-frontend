exports.exporterHeader = (token, organisationId) => {
  return {
    'ORGANISATION-ID': organisationId,
    'EXPORTER-USER-TOKEN': token,
    'Content-Type': 'application/json'
  }
}
