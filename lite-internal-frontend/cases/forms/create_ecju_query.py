from django.urls import reverse

from core.components import PicklistPicker
from lite_content.lite_internal_frontend import generic
from lite_content.lite_internal_frontend.cases import EcjuQueries
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import Form, BackLink, TextArea, RadioButtons, FormGroup, Option
from picklists.services import get_picklists_for_input


class ECJUQueryTypes:
    ECJU_QUERY = "ecju_query"
    PRE_VISIT_QUESTIONNAIRE = "pre_visit_questionnaire"
    COMPLIANCE_ACTION = "compliance_actions"

    choices = [
        (ECJU_QUERY, EcjuQueries.Queries.ECJU_QUERY),
        (PRE_VISIT_QUESTIONNAIRE, EcjuQueries.Queries.PRE_VISIT_QUESTIONNAIRE),
        (COMPLIANCE_ACTION, EcjuQueries.Queries.COMPLIANCE_ACTION),
    ]

    @classmethod
    def get_text(cls, choice):
        for key, value in cls.choices:
            if key == choice:
                return value
        return ""


def new_ecju_query_form(request, queue_pk, pk):
    query_type = request.POST.get("query_type", "")
    return FormGroup(
        [
            Form(
                title=cases.EcjuQueries.AddQuery.SELECT_A_TYPE,
                questions=[
                    RadioButtons(
                        name="query_type", options=[Option(choice[0], choice[1]) for choice in ECJUQueryTypes.choices],
                    )
                ],
                back_link=BackLink(
                    url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "ecju-queries"})
                ),
                default_button_name=generic.CONTINUE,
                container="case",
            ),
            Form(
                title=EcjuQueries.AddQuery.TITLE_PREFIX + ECJUQueryTypes.get_text(query_type).lower(),
                questions=[
                    TextArea(
                        description=cases.EcjuQueries.AddQuery.DESCRIPTION,
                        name="question",
                        extras={"max_length": 5000,},
                        data_attributes={"picklist-picker": query_type},
                    ),
                    PicklistPicker(target="question", items=get_picklists_for_input(request, query_type)),
                ],
                default_button_name=cases.EcjuQueries.AddQuery.SUBMIT,
                container="case",
            ),
        ]
    )
