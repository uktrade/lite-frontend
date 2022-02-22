exports.exporter = (token, organisationId) => {
  return {
    'ORGANISATION-ID': organisationId,
    'EXPORTER-USER-TOKEN': token,
    'Content-Type': 'application/json'
  }
}

exports.caseworker = (token) => {
  return { 'GOV-USER-TOKEN': token }
}
