from datetime import datetime


def get_initial_f1686_details(application):
    f1686_approval_date = application["f1686_approval_date"]
    if f1686_approval_date:
        f1686_approval_date = datetime.fromisoformat(application["f1686_approval_date"]).date()
    return {
        "f1686_contracting_authority": application["f1686_contracting_authority"],
        "f1686_reference_number": application["f1686_reference_number"],
        "f1686_approval_date": f1686_approval_date,
    }


def get_initial_other_security_approval_details(application):
    return {"other_security_approval_details": application["other_security_approval_details"]}


def get_initial_subject_to_itar_controls(application):
    return {"subject_to_itar_controls": application["subject_to_itar_controls"]}


def get_initial_f680_reference_number(application):
    return {"f680_reference_number": application["f680_reference_number"]}


def get_initial_security_classified_details(application):
    return {
        "is_mod_security_approved": application["is_mod_security_approved"],
        "security_approvals": application["security_approvals"],
    }
