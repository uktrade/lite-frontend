from core.wizard.payloads import MergingPayloadBuilder

from .constants import AddGoodComponentSteps, AddGoodComponentToApplicationSteps
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_payload,
    get_pv_grading_details_payload,
    get_part_number_payload,
    get_quantity_and_value_payload,
)
from core.constants import ComponentAccessoryChoices


def get_component_payload(form):
    component_payload = {}
    component_type_clean_data = form.cleaned_data["component_type"]
    details = (
        (ComponentAccessoryChoices.DESIGNED.value, "designed_details"),
        (ComponentAccessoryChoices.MODIFIED.value, "modified_details"),
        (ComponentAccessoryChoices.GENERAL.value, "general_details"),
    )
    for is_component, details_field in details:
        if component_type_clean_data == is_component:
            component_details = form.cleaned_data[details_field]
            if component_details:
                component_payload = {
                    "is_component": component_type_clean_data,
                    details_field: component_details,
                }
    return component_payload


def get_is_component_payload(form):
    if form.cleaned_data["is_component"]:
        # component details will be used to fill details
        return {}
    else:
        return {
            "is_component": "no",
        }


class AddGoodComponentPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodComponentSteps.NAME: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddGoodComponentSteps.IS_COMPONENT: get_is_component_payload,
        AddGoodComponentSteps.COMPONENT_DETAILS: get_component_payload,
        AddGoodComponentSteps.PART_NUMBER: get_part_number_payload,
        AddGoodComponentSteps.PV_GRADING: get_pv_grading_payload,
        AddGoodComponentSteps.PV_GRADING_DETAILS: get_pv_grading_details_payload,
        AddGoodComponentSteps.PRODUCT_USES_INFORMATION_SECURITY: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_AVAILABILITY: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_MILITARY_USE: get_cleaned_data,
        AddGoodComponentSteps.PRODUCT_DESCRIPTION: get_cleaned_data,
    }


class AddGoodComponentToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodComponentToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.QUANTITY_AND_VALUE: get_quantity_and_value_payload,
    }


def get_onward_incorporated_payload(form):
    cleaned_data = get_cleaned_data(form)

    return {
        "is_good_incorporated": form.cleaned_data["is_onward_incorporated"],
        **cleaned_data,
    }


class ComponentAccessoryProductOnApplicationSummaryEditOnwardExportedPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodComponentToApplicationSteps.ONWARD_EXPORTED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED: get_cleaned_data,
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED: get_onward_incorporated_payload,
    }


class ProductEditComponentDetailsPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddGoodComponentSteps.IS_COMPONENT: get_is_component_payload,
        AddGoodComponentSteps.COMPONENT_DETAILS: get_component_payload,
    }
