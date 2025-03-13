from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps

from .forms import (
    ApprovalTypeForm,
    ProductNameForm,
    ProductDescription,
    ProductForeignTechOrSharedInformation,
    ProductControlledUnderItar,
    ProductControlledUnderItarDetails,
    ProductIncludeCryptography,
    ProductRatedUnderMTCR,
    ProductMANPADs,
    ProductElectronicMODData,
    ProductFunding,
    ModSponsorDetails,
    ProductUsedByUKArmedForces,
)


class ApprovalTypeView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.APPROVAL_TYPE, ApprovalTypeForm),
    ]
    section = "approval_type"
    section_label = "Approval type"


def is_foreign_tech_or_information_shared(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED) or {}
    return cleaned_data.get("is_foreign_tech_or_information_shared", False)


def is_controlled_under_itar(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR) or {}
    return cleaned_data.get("is_controlled_under_itar", False)


def has_mod_sponsor(wizard):
    mod_sources = ["mod", "part_mod"]
    cleaned_data = wizard.get_cleaned_data_for_step(FormSteps.PRODUCT_FUNDING) or {}
    funding_source = cleaned_data.get("funding_source", "")
    result = False
    if funding_source in mod_sources:
        result = True

    return result


class ProductInformationView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.PRODUCT_NAME, ProductNameForm),
        (FormSteps.PRODUCT_DESCRIPTION, ProductDescription),
        (FormSteps.PRODUCT_FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED, ProductForeignTechOrSharedInformation),
        (FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR, ProductControlledUnderItar),
        (FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR_DETAILS, ProductControlledUnderItarDetails),
        (FormSteps.PRODUCT_INCLUDE_CRYPTOGRAPHY, ProductIncludeCryptography),
        (FormSteps.PRODUCT_RATED_UNDER_MTCR, ProductRatedUnderMTCR),
        (FormSteps.PRODUCT_MANPAD, ProductMANPADs),
        (FormSteps.PRODUCT_ELECTRONICMODDATA, ProductElectronicMODData),
        (FormSteps.PRODUCT_FUNDING, ProductFunding),
        (FormSteps.MOD_SPONSOR_DETAILS, ModSponsorDetails),
        (FormSteps.PRODUCT_USED_BY_UK_ARMED_FORCES, ProductUsedByUKArmedForces),
    ]
    condition_dict = {
        FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR: is_foreign_tech_or_information_shared,
        FormSteps.PRODUCT_CONTROLLED_UNDER_ITAR_DETAILS: is_controlled_under_itar,
        FormSteps.MOD_SPONSOR_DETAILS: has_mod_sponsor,
    }
    section = "product_information"
    section_label = "Product information"
