from exporter.core.wizard.payloads import MergingPayloadBuilder

from .constants import SecurityApprovalSteps
from exporter.applications.views.goods.common.payloads import get_cleaned_data


def get_f1686_data(form):
    payload = form.cleaned_data.copy()
    payload["f1686_approval_date"] = payload["f1686_approval_date"].isoformat()
    return payload


class SecurityApprovalStepsPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        SecurityApprovalSteps.SECURITY_CLASSIFIED: get_cleaned_data,
        SecurityApprovalSteps.F680_REFERENCE_NUMBER: get_cleaned_data,
        SecurityApprovalSteps.F1686_DETAILS: get_f1686_data,
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS: get_cleaned_data,
    }
