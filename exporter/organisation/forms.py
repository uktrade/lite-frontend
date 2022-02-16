from dateutil.relativedelta import relativedelta

from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit, Layout, HTML


def validate_expiry_date(value):
    today = timezone.now().date()
    if value < today:
        raise ValidationError("Expiry date must be in the future")
    else:
        if relativedelta(value, today).years >= 5:
            raise ValidationError("Expiry date is too far in the future")


class UploadSectionFiveCertificateForm(forms.Form):
    file = forms.FileField(
        label="",
        help_text="The file must be smaller than 50MB",
        error_messages={"required": "Select certificate file to upload"},
    )
    reference_code = forms.CharField(
        label="Certificate number",
        error_messages={"required": "Enter the certificate number"},
    )
    expiry_date = DateInputField(
        label="Expiry date",
        help_text="For example 12 3 2021",
        require_all_fields=False,
        validators=[validate_expiry_date],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1("Attach your section five certificate"),
            "file",
            "reference_code",
            "expiry_date",
            Submit("submit", "Submit"),
        )
        self.fields["expiry_date"].fields[2].error_messages["incomplete"] = "Enter the expiry year"
        self.fields["expiry_date"].fields[1].error_messages["incomplete"] = "Enter the expiry month"
        self.fields["expiry_date"].fields[0].error_messages["incomplete"] = "Enter the expiry day"


class UploadFirearmsCertificateForm(forms.Form):
    file = forms.FileField(
        label="",
        help_text="The file must be smaller than 50MB",
        error_messages={"required": "Select certificate file to upload"},
    )
    reference_code = forms.CharField(
        label="Certificate number",
        error_messages={"required": "Enter the certificate number"},
    )
    expiry_date = DateInputField(
        label="Expiry date",
        help_text="For example 12 3 2021",
        require_all_fields=False,
        validators=[validate_expiry_date],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1("Attach your registered firearms dealer certificate"),
            "file",
            "reference_code",
            "expiry_date",
            Submit("submit", "Submit"),
        )
        self.fields["expiry_date"].fields[2].error_messages["incomplete"] = "Enter the expiry year"
        self.fields["expiry_date"].fields[1].error_messages["incomplete"] = "Enter the expiry month"
        self.fields["expiry_date"].fields[0].error_messages["incomplete"] = "Enter the expiry day"
