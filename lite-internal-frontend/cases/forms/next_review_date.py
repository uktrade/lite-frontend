from django.urls import reverse

from lite_content.lite_internal_frontend import cases
from lite_forms.components import Form, BackLink, DateInput, Button


def set_next_review_date_form(queue_id, case_id):
    return Form(
        title=cases.Manage.SetNextReviewDate.TITLE,
        description=cases.Manage.SetNextReviewDate.DESCRIPTION,
        questions=[DateInput(prefix="next_review_date", name="next_review_date")],
        buttons=[Button("Continue", action="submit")],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id, "tab": "details"})),
    )
