from datetime import datetime
from django import forms
from django.forms.formsets import formset_factory

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Button
from crispy_forms_gds.fields import DateInputField

from django.urls import reverse_lazy

import lite_content.lite_internal_frontend.advice
from lite_forms.components import Form, TextInput, BackLink, DateInput, Label, HiddenField, Custom
from lite_forms.helpers import conditional


def get_formset(form_class, num=1, data=None, initial=None):
    factory = formset_factory(form_class, extra=num, min_num=num, max_num=num)
    return factory(data=data, initial=initial)


def approve_licence_form(queue_pk, case_id, editable_duration, goods, goods_html):
    return Form(
        title=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.APPROVE_TITLE,
        questions=[
            DateInput(
                description="For example, 27 3 2019",
                title=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.DATE_TITLE,
                prefix="",
            ),
            conditional(
                editable_duration,
                TextInput(
                    title=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.DURATION_TITLE,
                    name="duration",
                    description=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.DURATION_DESCRIPTION,
                ),
            ),
            HiddenField(name="action", value="approve"),
            conditional(
                goods,
                Custom(
                    goods_html,
                    data=goods,
                ),
            ),
        ],
        container="case",
        back_link=BackLink(
            url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case_id, "tab": "final-advice"}),
            text=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
        ),
    )


class GoodQuantityValueForm(forms.Form):
    quantity = forms.FloatField()
    value = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].widget.attrs["class"] = "govuk-input js-update-total-value"
        self.fields["value"].widget.attrs["class"] = "govuk-input"


class ApproveLicenceForm(forms.Form):
    DOCUMENT_TITLE = "Approve"
    CASE_TYPES = [("oiel", "OIEL"), ("siel", "SIEL")]

    case_type = forms.ChoiceField(label="Type of licence", choices=CASE_TYPES)
    date = DateInputField(
        label="Licence start date",
        help_text=f"For example, 20 2 {datetime.now().year}",
    )

    duration = forms.CharField(
        label="How long will it last",
        help_text="This must be a whole number of months, such as 12 or 24.",
        disabled=True,
    )

    def __init__(self, *args, **kwargs):
        # todo make use of editable
        editable_duration = kwargs.get("editable_duration")
        if editable_duration:
            del kwargs["editable_duration"]
        super().__init__(*args, **kwargs)
        if editable_duration:
            self.fields["duration"].disabled = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "case_type",
            "date",
            "duration",
        )


class ReissueLicenceForm(ApproveLicenceForm):
    pass


class DenyLicenceForm(forms.Form):
    title = "Finalise"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Button("submit", "Submit", css_class="govuk-!-margin-bottom-0"),
        )


def deny_licence_form(queue_pk, case_id, nlr):
    if nlr:
        description = "You'll be informing the exporter that no licence is required"
    else:
        description = "You'll be denying the case"

    return Form(
        title=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.FINALISE_TITLE,
        questions=[Label(description), HiddenField(name="action", value="refuse")],
        back_link=BackLink(
            url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case_id, "tab": "final-advice"}),
            text=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
        ),
    )
