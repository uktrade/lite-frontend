from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import ProductNameForm, ProductDescription, ProductClassification


class ProductInformationView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.PRODUCT_NAME, ProductNameForm),
        (FormSteps.PRODUCT_DESCRIPTION, ProductDescription),
        (FormSteps.SECURITY_GRADING_OR_CLASSIFICATION, ProductClassification),
    ]
    section = "approval_details"
