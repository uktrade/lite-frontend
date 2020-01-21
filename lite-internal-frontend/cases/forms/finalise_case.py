from django.urls import reverse_lazy
from lite_forms.components import Form, TextInput, BackLink, DateInput, Label
from lite_forms.helpers import conditional
from lite_content.lite_internal_frontend import cases


def approve_licence_form(case_id, standard, duration, editable_duration):
    return Form(
        title="Approve",
        questions=[
            DateInput(title=cases.FinalisePage.Date.TITLE, description=cases.FinalisePage.Date.DESCRIPTION, prefix="",),
            conditional(
                editable_duration,
                TextInput(
                    title=cases.FinalisePage.Duration.TITLE,
                    name="licence_duration",
                    description=cases.FinalisePage.Duration.DESCRIPTION,
                ),
                Label(text=f"Duration: {duration} months"),
            ),
        ],
        back_link=conditional(
            standard,
            BackLink(
                url=reverse_lazy("cases:final_advice_view", kwargs={"pk": case_id}),
                text=cases.FinalisePage.BackLink.FINAL_ADVICE,
            ),
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"pk": case_id}),
                text=cases.FinalisePage.BackLink.GOODS_AND_COUNTRIES,
            ),
        ),
    )


def refuse_licence_form(case_id, standard):
    return Form(
        title="Refuse",
        back_link=conditional(
            standard,
            BackLink(
                url=reverse_lazy("cases:final_advice_view", kwargs={"pk": case_id}),
                text=cases.FinalisePage.BackLink.FINAL_ADVICE,
            ),
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"pk": case_id}),
                text=cases.FinalisePage.BackLink.GOODS_AND_COUNTRIES,
            ),
        ),
    )
