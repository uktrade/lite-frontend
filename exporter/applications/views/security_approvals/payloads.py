from core.wizard.payloads import MergingPayloadBuilder

from .constants import SecurityApprovalSteps
from exporter.applications.views.goods.common.payloads import get_cleaned_data, get_questions_data


def get_f1686_data(form):
    payload = form.cleaned_data.copy()
    payload["f1686_approval_date"] = payload["f1686_approval_date"].isoformat()
    return payload


class SecurityApprovalStepsAnswerPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        SecurityApprovalSteps.SECURITY_CLASSIFIED: get_cleaned_data,
        SecurityApprovalSteps.SUBJECT_TO_ITAR_CONTROLS: get_cleaned_data,
        SecurityApprovalSteps.F680_REFERENCE_NUMBER: get_cleaned_data,
        SecurityApprovalSteps.F1686_DETAILS: get_f1686_data,
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS: get_cleaned_data,
    }


class SecurityApprovalStepsQuestionPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        SecurityApprovalSteps.SECURITY_CLASSIFIED: get_questions_data,
        SecurityApprovalSteps.SUBJECT_TO_ITAR_CONTROLS: get_questions_data,
        SecurityApprovalSteps.F680_REFERENCE_NUMBER: get_questions_data,
        SecurityApprovalSteps.F1686_DETAILS: get_questions_data,
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS: get_questions_data,
    }
