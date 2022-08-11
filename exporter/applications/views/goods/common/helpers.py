def get_product_document(good):
    is_document_available = good["is_document_available"]
    is_document_sensitive = good["is_document_sensitive"]
    if not is_document_available or (is_document_available and is_document_sensitive):
        return None

    if not good["documents"]:
        return None

    # when creating new product we can only add one document but we save it as
    # a list because from the product detail page user can add multiple documents
    return good["documents"][0]
