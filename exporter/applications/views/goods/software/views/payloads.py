from core.wizard.payloads import MergingPayloadBuilder

from .constants import AddGoodTechnologySteps, AddGoodTechnologyToApplicationSteps
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


class AddGoodTechnologyPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodTechnologySteps.NAME: get_cleaned_data,
        AddGoodTechnologySteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodTechnologySteps.PART_NUMBER: get_part_number_payload,
        AddGoodTechnologySteps.PV_GRADING: get_pv_grading_payload,
        AddGoodTechnologySteps.PV_GRADING_DETAILS: get_pv_grading_details_payload,
        AddGoodTechnologySteps.SECURITY_FEATURES: get_security_features_payload,
        AddGoodTechnologySteps.PRODUCT_DECLARED_AT_CUSTOMS: get_cleaned_data,
        AddGoodTechnologySteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodTechnologySteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodTechnologySteps.PRODUCT_DESCRIPTION: get_cleaned_data,
        AddGoodTechnologySteps.PRODUCT_MILITARY_USE: get_cleaned_data,
    }


class AddGoodTechnologyToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodTechnologyToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodTechnologyToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodTechnologyToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodTechnologyToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }


def get_onward_incorporated_payload(form):
    cleaned_data = get_cleaned_data(form)

    return {
        "is_good_incorporated": form.cleaned_data["is_onward_incorporated"],
        **cleaned_data,
    }


class TechnologyProductOnApplicationSummaryEditOnwardExportedPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodTechnologyToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodTechnologyToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodTechnologyToApplicationSteps.ONWARD_INCORPORATED: get_onward_incorporated_payload,
    }
