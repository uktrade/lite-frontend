from django.urls import reverse_lazy
from lite_forms.components import Form, TextInput, BackLink, DateInput, Label, HiddenField
from lite_forms.helpers import conditional
from lite_content.lite_internal_frontend import cases


def approve_licence_form(queue_pk, case_id, is_open_licence, duration, editable_duration):
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
                    name="duration",
                    description=cases.FinaliseLicenceForm.DURATION_DESCRIPTION,
                ),
                Label(text=f"Duration: {duration} months"),
            ),
            HiddenField(name="action", value="approve"),
        ],
        back_link=conditional(
            is_open_licence,
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"queue_pk": queue_pk, "pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_DECISION_MATRIX_BUTTON,
            ),
            BackLink(
                url=reverse_lazy("cases:final_advice_view", kwargs={"queue_pk": queue_pk, "pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
            ),
        ),
    )


def deny_licence_form(queue_pk, case_id, is_open_licence):
    return Form(
        title=cases.FinaliseLicenceForm.FINALISE_TITLE,
        questions=[HiddenField(name="action", value="refuse")],
        back_link=conditional(
            is_open_licence,
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"queue_pk": queue_pk, "pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_DECISION_MATRIX_BUTTON,
            ),
            BackLink(
                url=reverse_lazy("cases:final_advice_view", kwargs={"queue_pk": queue_pk, "pk": case_id}),
                text=cases.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
            ),
        ),
    )
