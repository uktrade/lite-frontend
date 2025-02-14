from exporter.f680.application_sections.views import F680ApplicationSectionWizard

from .constants import FormSteps
from .forms import ApprovalTypeForm, ProductNameForm


class ApprovalTypeView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.APPROVAL_TYPE, ApprovalTypeForm),
    ]
    section = "approval_details"


class ProductInformationView(F680ApplicationSectionWizard):
    form_list = [
        (FormSteps.PRODUCT_NAME, ProductNameForm),
    ]
    section = "approval_details"
