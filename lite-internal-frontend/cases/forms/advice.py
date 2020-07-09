from datetime import datetime, date

from django.urls import reverse

from cases.constants import CaseType
from cases.forms.finalise_case import approve_licence_form
from cases.objects import Case
from cases.services import get_application_default_duration
from conf.constants import Permission
from core import helpers
from core.components import PicklistPicker
from core.helpers import has_permission
from core.services import get_pv_gradings
from lite_content.lite_internal_frontend import advice
from lite_content.lite_internal_frontend.advice import GoodsDecisionMatrixPage, GenerateGoodsDecisionForm
from lite_forms.components import (
    Form,
    RadioButtons,
    Option,
    BackLink,
    TextArea,
    Checkboxes,
    HelpSection,
    HTMLBlock,
    Group,
    Custom,
    Select,
)
from lite_forms.helpers import conditional
from picklists.enums import PicklistCategories


def give_advice_form(request, case: Case, tab, queue_pk, denial_reasons, show_warning=False):
    return Form(
        title=advice.GiveOrChangeAdvicePage.TITLE,
        questions=[
            conditional(
                show_warning,
                HTMLBlock(
                    "<div class='govuk-warning-text'>"
                    + "<span class='govuk-warning-text__icon' aria-hidden='true'>!</span>"
                    + "<strong class='govuk-warning-text__text'>"
                    + "<span class='govuk-warning-text__assistive'>Warning</span>"
                    + advice.GiveOrChangeAdvicePage.WARNING
                    + "</strong>"
                    + "</div>"
                ),
            ),
            RadioButtons(
                name="type",
                description="<noscript>" + advice.GiveOrChangeAdvicePage.RadioButtons.DESCRIPTION + "</noscript>",
                options=[
                    Option(
                        key="approve",
                        value=advice.GiveOrChangeAdvicePage.RadioButtons.GRANT,
                        components=[
                            conditional(
                                CaseType.is_mod(case["case_type"]["sub_type"]["key"]),
                                Select(
                                    name="pv_grading_approve",
                                    title=advice.GiveOrChangeAdvicePage.GRADING_TITLE,
                                    options=get_pv_gradings(request, convert_to_options=True),
                                ),
                            )
                        ],
                    ),
                    Option(
                        key="proviso",
                        value=advice.GiveOrChangeAdvicePage.RadioButtons.PROVISO,
                        components=[
                            conditional(
                                CaseType.is_mod(case["case_type"]["sub_type"]["key"]),
                                Select(
                                    name="pv_grading_proviso",
                                    title=advice.GiveOrChangeAdvicePage.GRADING_TITLE,
                                    options=get_pv_gradings(request, convert_to_options=True),
                                ),
                            ),
                            TextArea(
                                title=advice.GiveOrChangeAdvicePage.PROVISO,
                                description=advice.GiveOrChangeAdvicePage.PROVISO_DESCRIPTION,
                                extras={"max_length": 5000},
                                name="proviso",
                            ),
                            PicklistPicker(target="proviso", type=PicklistCategories.proviso.key),
                        ],
                    ),
                    Option(
                        key="refuse",
                        value=conditional(
                            case.sub_type == CaseType.OPEN.value,
                            advice.GiveOrChangeAdvicePage.RadioButtons.REJECT,
                            advice.GiveOrChangeAdvicePage.RadioButtons.REFUSE,
                        ),
                        components=[
                            Group(
                                [
                                    Checkboxes(
                                        title=conditional(
                                            key == "1", advice.GiveOrChangeAdvicePage.DENIAL_REASONS_TITLE
                                        ),
                                        name="denial_reasons[]",
                                        options=denial_reasons[key],
                                        classes=["govuk-checkboxes--small", "govuk-checkboxes--inline"],
                                    )
                                    for key in denial_reasons.keys()
                                ],
                                ["app-advice__checkboxes"],
                            )
                        ],
                    ),
                    Option(key="no_licence_required", value=advice.GiveOrChangeAdvicePage.RadioButtons.NLR),
                    Option(
                        key="not_applicable",
                        value=advice.GiveOrChangeAdvicePage.RadioButtons.NOT_APPLICABLE,
                        show_or=True,
                    ),
                ],
            ),
            TextArea(title=advice.GiveOrChangeAdvicePage.REASON, extras={"max_length": 5000}, name="text"),
            PicklistPicker(target="text", type=PicklistCategories.standard_advice.key),
            TextArea(
                title=advice.GiveOrChangeAdvicePage.NOTE,
                description=advice.GiveOrChangeAdvicePage.NOTE_DESCRIPTION,
                optional=True,
                extras={"max_length": 200},
                name="note",
            ),
            conditional(
                has_permission(request, Permission.MAINTAIN_FOOTNOTES) and tab != "final-advice",
                RadioButtons(
                    title=advice.GiveOrChangeAdvicePage.FootNote.FOOTNOTE_REQUIRED,
                    name="footnote_required",
                    options=[
                        Option(
                            True,
                            advice.GiveOrChangeAdvicePage.FootNote.YES_OPTION,
                            components=[
                                TextArea(name="footnote"),
                                PicklistPicker(target="footnote", type=PicklistCategories.footnotes.key),
                            ],
                        ),
                        Option(False, advice.GiveOrChangeAdvicePage.FootNote.NO_OPTION),
                    ],
                ),
            ),
        ],
        default_button_name=advice.GiveOrChangeAdvicePage.Actions.CONTINUE_BUTTON,
        back_link=BackLink(
            advice.GiveOrChangeAdvicePage.Actions.BACK_BUTTON,
            reverse(f"cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"], "tab": tab}),
        ),
        container="case",
        helpers=[
            HelpSection(
                advice.GiveOrChangeAdvicePage.GIVING_ADVICE_ON, "", includes="case/includes/selection-sidebar.html"
            )
        ],
        javascript_imports={"/javascripts/advice.js"},
    )


def generate_documents_form():
    return Form(
        GenerateGoodsDecisionForm.TITLE,
        questions=[Custom("components/finalise-generate-documents.html")],
        container="case",
        default_button_name=GenerateGoodsDecisionForm.BUTTON,
    )


def finalise_goods_countries_form(**kwargs):
    return Form(
        title=GoodsDecisionMatrixPage.TITLE,
        questions=[Custom("components/finalise-goods-countries-table.html")],
        back_link=BackLink(
            url=reverse(
                "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "final-advice"}
            )
        ),
        container="case",
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
        is_open_licence=case.data["case_type"]["sub_type"]["key"] == CaseType.OPEN.value,
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
        is_open_licence=case.data["case_type"]["sub_type"]["key"] == CaseType.OPEN.value,
        editable_duration=helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION),
        goods=goods,
        goods_html="components/goods-licence-list.html",
    )
    return form, data
