from django.urls import reverse

from lite_content.lite_internal_frontend.cases import Manage
from lite_forms.components import Form, TextArea, RadioButtons, DetailComponent, BackLink, Option


def reissue_ogl_confirmation_form(case_id, queue_id):
    return Form(
        title=Manage.ReissueOGL.TITLE,
        description=Manage.ReissueOGL.DESCRIPTION,
        questions=[
            RadioButtons(
                name="confirm",
                options=[Option(key=True, value=Manage.ReissueOGL.YES), Option(key=False, value=Manage.ReissueOGL.NO)],
                classes=["govuk-checkboxes--inline"],
            ),
            DetailComponent(
                title=Manage.ReissueOGL.NOTE,
                components=[TextArea(name="note", classes=["govuk-!-margin-0"])],
            ),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id})),
        default_button_name=Manage.ReissueOGL.SUBMIT,
        container="case",
    )
