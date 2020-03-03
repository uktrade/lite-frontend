from applications.services import (
    post_party_document,
    get_party_document,
    delete_party_document,
    post_additional_document,
    get_additional_document,
    delete_additional_party_document,
)
from lite_content.lite_exporter_frontend import strings


def document_switch(path):
    if "ultimate-end-user" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:ultimate_end_users",
            "strings": strings.UltimateEndUser.Documents.AttachDocuments,
        }
    elif "end-user" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:end_user",
            "strings": strings.EndUser.Documents.AttachDocuments,
        }
    elif "consignee" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:consignee",
            "strings": strings.Consignee.Documents.AttachDocuments,
        }
    elif "third-parties" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:third_parties",
            "strings": strings.ThirdParties.Documents.AttachDocuments,
        }
    elif "additional-document" in path:
        return {
            "attach": post_additional_document,
            "download": get_additional_document,
            "delete": delete_additional_party_document,
            "homepage": "applications:additional_documents",
            "strings": strings.AdditionalDocuments.Documents.AttachDocuments,
        }
    else:
        raise NotImplementedError("document_switch doesn't support this document type")
