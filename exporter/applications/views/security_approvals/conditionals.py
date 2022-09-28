from core.constants import SecurityClassifiedApprovalsType
from .constants import SecurityApprovalSteps


def is_f680_approval(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SecurityApprovalSteps.SECURITY_CLASSIFIED)
    return SecurityClassifiedApprovalsType.F680 in cleaned_data.get("security_approvals", [])


def is_f1686_approval(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SecurityApprovalSteps.SECURITY_CLASSIFIED)
    return SecurityClassifiedApprovalsType.F1686 in cleaned_data.get("security_approvals", [])


def is_other_approval(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SecurityApprovalSteps.SECURITY_CLASSIFIED)
    return SecurityClassifiedApprovalsType.OTHER in cleaned_data.get("security_approvals", [])


def is_f680_approval_changed_and_selected(wizard):

    cleaned_data = wizard.get_cleaned_data_for_step(SecurityApprovalSteps.SECURITY_CLASSIFIED)
    return (
        SecurityClassifiedApprovalsType.F680 in cleaned_data.get("security_approvals", [])
        and not SecurityClassifiedApprovalsType.F680 in wizard.application.security_approvals
    )


def is_f1686_approval_changed_and_selected(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SecurityApprovalSteps.SECURITY_CLASSIFIED)
    return (
        SecurityClassifiedApprovalsType.F1686 in cleaned_data.get("security_approvals", [])
        and not SecurityClassifiedApprovalsType.F1686 in wizard.application.security_approvals
    )


def is_other_approval_changed_and_selected(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SecurityApprovalSteps.SECURITY_CLASSIFIED)
    return (
        SecurityClassifiedApprovalsType.OTHER in cleaned_data.get("security_approvals", [])
        and not SecurityClassifiedApprovalsType.OTHER in wizard.application.security_approvals
    )
