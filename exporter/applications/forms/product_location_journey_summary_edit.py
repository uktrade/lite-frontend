from django import forms
from datetime import datetime
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit, Layout, HTML, Field, Div


class TemporaryExportDetailsForm(forms.Form):
    class Layout:
        TITLE = "Explain why the products are being exported temporarily"

    temp_export_details = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            "temp_export_details",
            Submit("submit", "Continue"),
        )


class TemporaryDirectControlForm(forms.Form):
    is_temp_direct_control = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect,
        choices=[(True, "Yes"), (False, "No")],
    )

    temp_direct_control_details = forms.CharField(
        label="Who will be in control of the products while overseas, and what is your relationship to them?",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )


class ProposedReturnDateForm(forms.Form):
    class Layout:
        TITLE = "Proposed date the products will return to the UK"

    day = forms.IntegerField(label="Day", widget=forms.NumberInput(attrs={"placeholder": "DD"}))
    month = forms.IntegerField(label="Month", widget=forms.NumberInput(attrs={"placeholder": "MM"}))
    year = forms.IntegerField(label="Year", widget=forms.NumberInput(attrs={"placeholder": "YYYY"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = datetime.now().year
        example_date = f"For example, 20 2 {current_year + 2}"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            HTML(f'<span for="proposed_return_date" class="govuk-hint">{example_date}</span>'),
            Div(
                Div(
                    Field("day", css_class="govuk-input govuk-date-input__input govuk-input--width-3"),
                    css_class="govuk-date-input__item",
                ),
                Div(
                    Field("month", css_class="govuk-input govuk-date-input__input govuk-input--width-3"),
                    css_class="govuk-date-input__item",
                ),
                Div(
                    Field("year", css_class="govuk-input govuk-date-input__input govuk-input--width-3"),
                    css_class="govuk-date-input__item",
                ),
                css_class="govuk-date-input",
                id="proposed_return_date",
            ),
            Submit("submit", "Continue"),
        )


class ShippedWaybillOrLadingViewForm(forms.Form):
    is_shipped_waybill_or_lading = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect,
        choices=[(True, "Yes"), (False, "No")],
    )

    non_waybill_or_lading_route_details = forms.CharField(
        label="Provide details of the route of the products",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )
