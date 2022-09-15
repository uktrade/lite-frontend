from exporter.core.wizard.payloads import MergingPayloadBuilder

from .constants import ExportDetailsSteps
from exporter.applications.views.goods.common.payloads import get_cleaned_data


def get_f1686_data(form):
    cleaned_data = form.cleaned_data

    payload = {"f1686_contracting_authority": cleaned_data["f1686_contracting_authority"]}
    if not cleaned_data["is_f1686_approval_document_available"]:
        payload.update(
            {
                "f1686_reference_number": cleaned_data["f1686_reference_number"],
                "f1686_approval_date": cleaned_data["f1686_approval_date"].isoformat(),
            }
        )

    return payload


def get_other_details_data(form):
    return {"other_security_approval_details": form.cleaned_data["other_security_approval_details"]}


class ExportDetailsStepsPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        ExportDetailsSteps.SECURITY_CLASSIFIED: get_cleaned_data,
        ExportDetailsSteps.F680_REFERENCE_NUMBER: get_cleaned_data,
        ExportDetailsSteps.F1686_DETAILS: get_f1686_data,
        ExportDetailsSteps.SECURITY_OTHER_DETAILS: get_other_details_data,
    }
