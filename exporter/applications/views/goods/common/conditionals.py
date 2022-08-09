from .constants import PV_GRADING, PRODUCT_DOCUMENT_AVAILABILITY, PRODUCT_DOCUMENT_SENSITIVITY


def is_pv_graded(wizard):
    add_goods_cleaned_data = wizard.get_cleaned_data_for_step(PV_GRADING)
    return add_goods_cleaned_data.get("is_pv_graded")


def is_product_document_available(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(PRODUCT_DOCUMENT_AVAILABILITY)
    return cleaned_data.get("is_document_available")


def is_document_sensitive(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(PRODUCT_DOCUMENT_SENSITIVITY)
    return cleaned_data.get("is_document_sensitive")
