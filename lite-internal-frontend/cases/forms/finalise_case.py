from django.urls import reverse_lazy
from lite_forms.components import Form, TextInput, BackLink, DateInput, Label
from lite_forms.helpers import conditional
from lite_content.lite_internal_frontend import cases


def approve_licence_form(case_id, standard, duration, editable_duration):
    return Form(
        title=cases.FinaliseLicenceForm.APPROVE_TITLE,
        questions=[
            DateInput(
                description=cases.FinaliseLicenceForm.DATE_DESCRIPTION,
                title=cases.FinaliseLicenceForm.DATE_TITLE,
                prefix="",
            ),
            conditional(
                editable_duration,
                TextInput(
                    title=cases.FinaliseLicenceForm.DURATION_TITLE,
                    name="licence_duration",
                    description=cases.FinaliseLicenceForm.DURATION_DESCRIPTION,
                ),
                Label(text=f"Duration: {duration} months"),
            ),
        ],
        back_link=conditional(
            standard,
            BackLink(
                url=reverse_lazy("cases:final_advice_view", kwargs={"pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
            ),
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_DECISION_MATRIX_BUTTON,
            ),
        ),
    )


def deny_licence_form(case_id, is_standard_licence):
    if is_standard_licence:
        title = cases.FinaliseLicenceForm.REFUSE_TITLE
    else:
        title = cases.FinaliseLicenceForm.REJECT_TITLE

    return Form(
        title=title,
        back_link=conditional(
            is_standard_licence,
            BackLink(
                url=reverse_lazy("cases:final_advice_view", kwargs={"pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
            ),
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_DECISION_MATRIX_BUTTON,
            ),
        ),
    )
