from core.wizard.payloads import MergingPayloadBuilder

from .constants import AddF680GoodDetailsSteps, AddF680GoodDetailsToApplicationSteps
from exporter.applications.views.goods.common.payloads import get_cleaned_data


def get_prospect_value_payload(form):
    return {
        "quantity": 1,
        "unit": "NAR",
        "value": str(form.cleaned_data["value"]),
    }


class AddF680GoodDetailsPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddF680GoodDetailsSteps.NAME: get_cleaned_data,
        AddF680GoodDetailsSteps.PRODUCT_CONTROL_LIST_ENTRY: get_cleaned_data,
        AddF680GoodDetailsSteps.PRODUCT_DESCRIPTION: get_cleaned_data,
    }


class AddF680GoodDetailsToApplicationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        AddF680GoodDetailsToApplicationSteps.PROSPECT_VALUE: get_prospect_value_payload,
    }
