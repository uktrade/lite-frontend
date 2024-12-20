from datetime import datetime, date

from django.urls import reverse

from caseworker.cases.forms.finalise_case import approve_licence_form
from caseworker.cases.services import get_application_default_duration
from caseworker.core.constants import Permission
from caseworker.core import helpers
from lite_content.lite_internal_frontend.advice import GenerateGoodsDecisionForm
from lite_forms.components import (
    Form,
    BackLink,
    TextArea,
    Custom,
    DetailComponent,
)


def generate_documents_form(queue_pk, case_pk):
    return Form(
        title=GenerateGoodsDecisionForm.TITLE,
        questions=[
            Custom("components/finalise-generate-documents.html"),
            DetailComponent(
                title=GenerateGoodsDecisionForm.NOTE,
                components=[
                    TextArea(
                        title=GenerateGoodsDecisionForm.NOTE_DESCRIPTION, name="note", classes=["govuk-!-margin-0"]
                    ),
                ],
            ),
        ],
        back_link=BackLink(url=reverse("cases:finalise", kwargs={"queue_pk": queue_pk, "pk": case_pk})),
        container="case",
        default_button_name=GenerateGoodsDecisionForm.BUTTON,
    )


def get_approve_data(request, case_id, licence=None):
    if licence:
        start_date = datetime.strptime(licence["start_date"], "%Y-%m-%d")
        duration = licence["duration"]
    else:
        start_date = date.today()
        duration = get_application_default_duration(request, str(case_id))

    return {
        "day": request.POST.get("day") or start_date.day,
        "month": request.POST.get("month") or start_date.month,
        "year": request.POST.get("year") or start_date.year,
        "duration": request.POST.get("duration") or duration,
    }


def reissue_finalise_form(request, licence, case, queue_pk):
    data = get_approve_data(request, str(case["id"]), licence)
    form = approve_licence_form(
        queue_pk=queue_pk,
        case_id=case["id"],
        editable_duration=helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION),
        goods=licence["goods_on_licence"],
        goods_html="components/goods-licence-reissue-list.html",
    )
    return form, data


def finalise_form(request, case, goods, queue_pk):
    data = get_approve_data(request, str(case["id"]))
    form = approve_licence_form(
        queue_pk=queue_pk,
        case_id=case["id"],
        editable_duration=helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION),
        goods=goods,
        goods_html="components/goods-licence-list.html",
    )
    return form, data
