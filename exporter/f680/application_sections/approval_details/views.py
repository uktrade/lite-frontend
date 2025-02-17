from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import ProductNameForm, ProductDescription, ForeignTechOrSharedInformation


class ProductInformationView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.PRODUCT_NAME, ProductNameForm),
        (FormSteps.PRODUCT_DESCRIPTION, ProductDescription),
        (FormSteps.FOREIGN_TECHNOLOGY_OR_INFORMATION_SHARED, ForeignTechOrSharedInformation),
    ]
    section = "approval_details"
