from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps

from .forms import (
    ApprovalTypeForm,
    ProductNameForm,
    ProductDescription,
    ForeignTechOrSharedInformation,
    ControlledUnderItar,
    AboutControlledUnderItar,
    IncludeCryptography,
    ItemRatedUnderMCTR,
)


class ApprovalTypeView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.APPROVAL_TYPE, ApprovalTypeForm),
    ]
    section = "approval_details"


def is_foreign_tech_or_information_shared(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED) or {}
    return cleaned_data.get("is_foreign_tech_or_information_shared", False)


def is_controlled_under_itar(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.CONTROLLED_UNDER_ITAR) or {}
    return cleaned_data.get("is_controlled_under_itar", False)


class ProductInformationView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.PRODUCT_NAME, ProductNameForm),
        (FormSteps.PRODUCT_DESCRIPTION, ProductDescription),
        (FormSteps.FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED, ForeignTechOrSharedInformation),
        (FormSteps.CONTROLLED_UNDER_ITAR, ControlledUnderItar),
        (FormSteps.ABOUT_CONTROLLED_UNDER_ITAR, AboutControlledUnderItar),
        (FormSteps.INCLUDE_CRYPTOGRAPHY, IncludeCryptography),
        (FormSteps.RATED_UNDER_MCTR, ItemRatedUnderMCTR),
    ]
    section = "approval_details"
    condition_dict = {
        FormSteps.CONTROLLED_UNDER_ITAR: is_foreign_tech_or_information_shared,
        FormSteps.ABOUT_CONTROLLED_UNDER_ITAR: is_controlled_under_itar,
    }
