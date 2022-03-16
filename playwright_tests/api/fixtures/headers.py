def exporter(token, organisationId):
    return {"ORGANISATION-ID": organisationId, "EXPORTER-USER-TOKEN": token, "Content-Type": "application/json"}


def caseworker(token):
    return {"GOV-USER-TOKEN": token}
