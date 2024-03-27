from exporter.applications.views.goods.common.payloads import get_cleaned_data
from core.wizard.payloads import MergingPayloadBuilder

from .constants import RegistrationSteps
from .forms import RegisterAddressDetailsUKForm


def get_address_details_payload(form):
    if isinstance(form, RegisterAddressDetailsUKForm):
        address = {
            "address_line_1": form.cleaned_data["address_line_1"],
            "address_line_2": form.cleaned_data["address_line_2"],
            "city": form.cleaned_data["city"],
            "region": form.cleaned_data["region"],
            "postcode": form.cleaned_data["postcode"],
        }
    else:
        address = {
            "address": form.cleaned_data["address"],
            "country": form.cleaned_data["country"],
        }
    return {
        "site": {"name": form.cleaned_data["name"], "address": address},
        "phone_number": form.cleaned_data["phone_number"],
        "website": form.cleaned_data["website"],
    }


class RegistrationPayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        RegistrationSteps.REGISTRATION_TYPE: get_cleaned_data,
        RegistrationSteps.UK_BASED: get_cleaned_data,
        RegistrationSteps.REGISTRATION_DETAILS: get_cleaned_data,
        RegistrationSteps.ADDRESS_DETAILS: get_address_details_payload,
    }
