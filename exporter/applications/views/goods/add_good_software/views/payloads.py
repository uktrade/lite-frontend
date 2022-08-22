from exporter.core.wizard.payloads import MergingPayloadBuilder

from .constants import AddGoodSoftwareSteps, AddGoodSoftwareToApplicationSteps
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_payload,
    get_pv_grading_details_payload,
    get_part_number_payload,
    get_quantity_and_value_payload,
)


def get_security_features_payload(form):
    if form.cleaned_data["has_security_features"]:
        return {
            "has_security_features": True,
            "security_feature_details": form.cleaned_data["security_feature_details"],
        }
    else:
        return {
            "has_security_features": False,
            "security_feature_details": "",
        }


class AddGoodSoftwarePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodSoftwareSteps.NAME: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodSoftwareSteps.PART_NUMBER: get_part_number_payload,
        AddGoodSoftwareSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodSoftwareSteps.PV_GRADING_DETAILS: get_pv_grading_details_payload,
        AddGoodSoftwareSteps.SECURITY_FEATURES: get_security_features_payload,
        AddGoodSoftwareSteps.PRODUCT_DECLARED_AT_CUSTOMS: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_DESIGN_DETAILS: get_cleaned_data,
        AddGoodSoftwareSteps.PRODUCT_MILITARY_USE: get_cleaned_data,
    }


class AddGoodSoftwareToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodSoftwareToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodSoftwareToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodSoftwareToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodSoftwareToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }
