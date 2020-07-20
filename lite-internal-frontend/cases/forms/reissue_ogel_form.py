from django.urls import reverse

from lite_content.lite_internal_frontend.cases import Manage
from lite_forms.generators import confirm_form


def reissue_ogel_confirmation_form(case_id, queue_id):
    return confirm_form(
        title=Manage.ReissueOGEL.TITLE,
        description=Manage.ReissueOGEL.DESCRIPTION,
        confirmation_name="confirm",
        back_link_text=Manage.ReissueOGEL.BACK,
        back_url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id}),
        yes_label=Manage.ReissueOGEL.YES,
        no_label=Manage.ReissueOGEL.NO,
        submit_button_text=Manage.ReissueOGEL.SUBMIT,
        container="case",
    )
