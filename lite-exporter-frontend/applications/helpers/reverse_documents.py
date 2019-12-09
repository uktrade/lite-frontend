from applications.services import (
    post_ultimate_end_user_document,
    post_end_user_document,
    get_ultimate_end_user_document,
    get_end_user_document,
    delete_ultimate_end_user_document,
    delete_end_user_document,
    post_consignee_document,
    get_consignee_document,
    delete_consignee_document,
    post_third_party_document,
    get_third_party_document,
    delete_third_party_document,
    post_additional_document,
    get_additional_document,
    delete_additional_party_document,
    post_goods_type_document,
    delete_goods_type_document,
    get_goods_type_document,
    get_generated_document,
)


def document_switch(path):
    if "ultimate-end-user" in path:
        return {
            "attach": post_ultimate_end_user_document,
            "download": get_ultimate_end_user_document,
            "delete": delete_ultimate_end_user_document,
            "homepage": "applications:ultimate_end_users",
            "strings": "ultimate_end_user.documents",
            "has_description": False,
        }
    elif "end-user" in path:
        return {
            "attach": post_end_user_document,
            "download": get_end_user_document,
            "delete": delete_end_user_document,
            "homepage": "applications:end_user",
            "strings": "end_user.documents",
            "has_description": False,
        }
    elif "consignee" in path:
        return {
            "attach": post_consignee_document,
            "download": get_consignee_document,
            "delete": delete_consignee_document,
            "homepage": "applications:consignee",
            "strings": "consignee.documents",
            "has_description": False,
        }
    elif "third-parties" in path:
        return {
            "attach": post_third_party_document,
            "download": get_third_party_document,
            "delete": delete_third_party_document,
            "homepage": "applications:third_parties",
            "strings": "third_parties.documents",
            "has_description": False,
        }
    elif "goods-type" in path:
        return {
            "attach": post_goods_type_document,
            "download": get_goods_type_document,
            "delete": delete_goods_type_document,
            "homepage": "applications:goods_types",
            "strings": "goods_types.documents",
            "has_description": False,
        }
    elif "additional-document" in path:
        return {
            "attach": post_additional_document,
            "download": get_additional_document,
            "delete": delete_additional_party_document,
            "homepage": "applications:additional_documents",
            "strings": "additional_documents.documents",
            "has_description": False,
        }
    elif "generated-documents" in path:
        return {
            "download": get_generated_document,
        }
    else:
        raise NotImplementedError("document_switch doesn't support this document type")
