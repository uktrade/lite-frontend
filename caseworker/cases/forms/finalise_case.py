from django.urls import reverse_lazy

import lite_content.lite_internal_frontend.advice
from lite_forms.components import Form, TextInput, BackLink, DateInput, Label, HiddenField, Custom
from lite_forms.helpers import conditional


def approve_licence_form(queue_pk, case_id, is_open_licence, editable_duration, goods, goods_html):
    return Form(
        title=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.APPROVE_TITLE,
        questions=[
            DateInput(
                description=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.DATE_DESCRIPTION,
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
        back_link=conditional(
            is_open_licence,
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"queue_pk": queue_pk, "pk": case_id}),
                text=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.Actions.BACK_TO_DECISION_MATRIX_BUTTON,
            ),
            BackLink(
                url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case_id, "tab": "final-advice"}),
                text=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
            ),
        ),
    )


def deny_licence_form(queue_pk, case_id, is_open_licence, nlr):
    if nlr:
        description = lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.NLR_DESCRIPTION
    else:
        description = lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.REFUSE_DESCRIPTION

    return Form(
        title=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.FINALISE_TITLE,
        questions=[Label(description), HiddenField(name="action", value="refuse")],
        back_link=conditional(
            is_open_licence,
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"queue_pk": queue_pk, "pk": case_id}),
                text=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.Actions.BACK_TO_DECISION_MATRIX_BUTTON,
            ),
            BackLink(
                url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case_id, "tab": "final-advice"}),
                text=lite_content.lite_internal_frontend.advice.FinaliseLicenceForm.Actions.BACK_TO_ADVICE_BUTTON,
            ),
        ),
    )
