from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import ProductNameForm


class ProductInformationView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.PRODUCT_NAME, ProductNameForm),
    ]
    section = "approval_details"
