from django.urls import reverse

from cases.constants import CaseType
from cases.objects import Case
from conf.constants import Permission
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
from picklists.services import get_picklists_for_input


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
                            PicklistPicker(target="proviso", items=get_picklists_for_input(request, "proviso")),
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
            PicklistPicker(target="text", items=get_picklists_for_input(request, "standard_advice")),
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
                                PicklistPicker(target="footnote", items=get_picklists_for_input(request, "footnotes")),
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
    )


def generate_documents_form():
    return Form(
        GenerateGoodsDecisionForm.TITLE,
        questions=[Custom("components/finalise-generate-documents.html")],
        container="case",
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
