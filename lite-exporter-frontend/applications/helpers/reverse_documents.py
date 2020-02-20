from applications.services import (
    post_party_document,
    get_party_document,
    delete_party_document,
    post_additional_document,
    get_additional_document,
    delete_additional_party_document,
    post_goods_type_document,
    delete_goods_type_document,
    get_goods_type_document,
)
from lite_content.lite_exporter_frontend import strings  # noqa


def document_switch(path):
    if "ultimate-end-user" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:ultimate_end_users",
            "has_description": False,
            "attach_doc_description_field_string": strings.UltimateEndUser.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
            "attach_doc_title_string": strings.UltimateEndUser.Documents.AttachDocuments.TITLE,
            "attach_doc_return_later_string": strings.UltimateEndUser.Documents.SAVE_END_USER,
            "delete_conf_back_link_string": strings.UltimateEndUser.Documents.AttachDocuments.BACK_TO_APPLICATION_OVERVIEW,
        }
    elif "end-user" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:end_user",
            "has_description": False,
            "attach_doc_description_field_string": strings.EndUser.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
            "attach_doc_title_string": strings.EndUser.Documents.AttachDocuments.TITLE,
            "attach_doc_return_later_string": strings.EndUser.Documents.SAVE_END_USER,
            "delete_conf_back_link_string": strings.EndUser.Documents.AttachDocuments.BACK_TO_APPLICATION_OVERVIEW,
        }
    elif "consignee" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:consignee",
            "has_description": False,
            "attach_doc_description_field_string": strings.Consignee.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
            "attach_doc_title_string": strings.Consignee.Documents.AttachDocuments.TITLE,
            "attach_doc_return_later_string": strings.Consignee.Documents.SAVE_END_USER,
            "delete_conf_back_link_string": strings.Consignee.Documents.AttachDocuments.BACK_TO_APPLICATION_OVERVIEW,
        }
    elif "third-parties" in path:
        return {
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:third_parties",
            "has_description": False,
            "attach_doc_description_field_string": strings.ThirdParties.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
            "attach_doc_title_string": strings.ThirdParties.Documents.AttachDocuments.TITLE,
            "attach_doc_return_later_string": strings.ThirdParties.Documents.SAVE_END_USER,
            "delete_conf_back_link_string": strings.ThirdParties.Documents.AttachDocuments.BACK_TO_APPLICATION_OVERVIEW,
        }
    elif "goods-type" in path:
        return {
            "attach": post_goods_type_document,
            "download": get_goods_type_document,
            "delete": delete_goods_type_document,
            "homepage": "applications:goods_types",
            "has_description": False,
            "attach_doc_description_field_string": strings.AdditionalDocuments.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
            "attach_doc_title_string": strings.AdditionalDocuments.Documents.AttachDocuments.TITLE,
            "attach_doc_return_later_string": strings.AdditionalDocuments.Documents.SAVE_END_USER,
            "delete_conf_back_link_string": strings.AdditionalDocuments.Documents.AttachDocuments.BACK_TO_APPLICATION_OVERVIEW,
        }
    elif "additional-document" in path:
        return {
            "attach": post_additional_document,
            "download": get_additional_document,
            "delete": delete_additional_party_document,
            "homepage": "applications:additional_documents",
            "has_description": False,
            "attach_doc_description_field_string": strings.AdditionalDocuments.Documents.AttachDocuments.DESCRIPTION_FIELD_TITLE,
            "attach_doc_title_string": strings.AdditionalDocuments.Documents.AttachDocuments.TITLE,
            "attach_doc_return_later_string": strings.AdditionalDocuments.Documents.SAVE_END_USER,
            "delete_conf_back_link_string": strings.AdditionalDocuments.Documents.AttachDocuments.BACK_TO_APPLICATION_OVERVIEW,
        }
    else:
        raise NotImplementedError("document_switch doesn't support this document type")
