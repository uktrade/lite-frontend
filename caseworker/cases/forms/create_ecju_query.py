from django.urls import reverse

from caseworker.core.components import PicklistPicker
from lite_content.lite_internal_frontend.cases import EcjuQueries
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import Form, TextArea, HiddenField, BackLink
from crispy_forms_gds.layout import Field, Layout, Size, Submit

from django.views.generic import FormView

from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit


class ECJUQueryTypes:
    ECJU_QUERY = "ecju_query"
    PRE_VISIT_QUESTIONNAIRE = "pre_visit_questionnaire"
    COMPLIANCE_ACTION = "compliance_actions"

    choices = [
        (ECJU_QUERY, EcjuQueries.Queries.ECJU_QUERY),
        (PRE_VISIT_QUESTIONNAIRE, EcjuQueries.Queries.PRE_VISIT_QUESTIONNAIRE),  # ?
        (COMPLIANCE_ACTION, EcjuQueries.Queries.COMPLIANCE_ACTION),  # ?
    ]

    @classmethod
    def get_text(cls, choice):
        for key, value in cls.choices:
            if key == choice:
                return value
        return ""


def new_ecju_query_form(queue_pk, pk, query_type):
    return Form(
        title=EcjuQueries.AddQuery.TITLE_PREFIX + ECJUQueryTypes.get_text(query_type).lower(),
        questions=[
            HiddenField("query_type", query_type),
            TextArea(
                description=cases.EcjuQueries.AddQuery.DESCRIPTION, name="question", extras={"max_length": 5000,},
            ),
            PicklistPicker(target="question", type=query_type),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "ecju-queries"})),
        default_button_name=cases.EcjuQueries.AddQuery.SUBMIT,
        container="case",
    )


class NewEcjuQueryFormCrispy(forms.Form):
    title = EcjuQueries.AddQuery.TITLE_PREFIX + ECJUQueryTypes.get_text("ecju_query").lower(),

    questions = forms.CharField(
        label=title,
        widget=forms.Textarea,
        help_text=cases.EcjuQueries.AddQuery.DESCRIPTION,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field.textarea(
                "questions",
                label_size=Size.LARGE,
                label_tag="h2",
                rows=10,
                max_length=5000,
            ),
            Submit("submit", "Submit"),
        )
