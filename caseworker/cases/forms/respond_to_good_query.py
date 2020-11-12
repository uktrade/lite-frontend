from django.urls import reverse_lazy

from core.builtins.custom_tags import default_na
from caseworker.core.components import PicklistPicker
from caseworker.core.services import get_control_list_entries, get_gov_pv_gradings
from lite_content.lite_internal_frontend.cases import CLCReviewGoods, PVGradingForm
from lite_forms.common import control_list_entries_question
from lite_forms.components import (
    Form,
    BackLink,
    RadioButtons,
    Option,
    TextArea,
    Heading,
    Group,
    TextInput,
    Select,
    Summary,
    DetailComponent,
)
from lite_forms.styles import HeadingStyle
from caseworker.picklists.enums import PicklistCategories


def respond_to_clc_query_form(request, queue_pk, case):
    if case.data["good"]["is_good_controlled"]:
        is_good_controlled = case.data["good"]["is_good_controlled"]["value"]
    else:
        is_good_controlled = None

    return Form(
        title=CLCReviewGoods.TITLE,
        description=CLCReviewGoods.DESCRIPTION,
        questions=[
            Heading(CLCReviewGoods.HEADING, HeadingStyle.S),
            Summary(
                values={
                    CLCReviewGoods.Summary.DESCRIPTION: case.data["good"]["description"],
                    CLCReviewGoods.Summary.PART_NUMBER: default_na(case.data["good"]["part_number"]),
                    CLCReviewGoods.Summary.IS_THIS_GOOD_CONTROLLED: is_good_controlled,
                    CLCReviewGoods.Summary.CONTROL_LIST_ENTRIES: case.data["clc_control_list_entry"],
                    CLCReviewGoods.Summary.EXPLANATION: case.data["clc_raised_reasons"],
                },
                classes=[
                    "govuk-inset-text",
                    "govuk-summary-list--no-border",
                    "govuk-!-padding-top-0",
                    "govuk-!-padding-bottom-0",
                    "govuk-!-padding-left-6",
                ],
            ),
            Heading(CLCReviewGoods.YOUR_RESPONSE, HeadingStyle.S),
            RadioButtons(
                title=CLCReviewGoods.Controlled.TITLE,
                name="is_good_controlled",
                classes=["govuk-radios--small"],
                options=[
                    Option(
                        key=True,
                        value="yes",
                        components=[
                            control_list_entries_question(
                                control_list_entries=get_control_list_entries(request, convert_to_options=True),
                                title=CLCReviewGoods.CONTROL_LIST_ENTRY,
                            ),
                            PicklistPicker(
                                target="report_summary",
                                title=CLCReviewGoods.ReportSummary.TITLE,
                                description=CLCReviewGoods.ReportSummary.DESCRIPTION,
                                type=PicklistCategories.report_summary.key,
                                set_text=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="no"),
                ],
            ),
            DetailComponent(
                title=PVGradingForm.COMMENT,
                components=[
                    TextArea(
                        name="comment",
                        extras={
                            "max_length": 500,
                        },
                    ),
                ],
            ),
        ],
        default_button_name=CLCReviewGoods.SUBMIT_BUTTON,
        back_link=BackLink(
            url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"]}),
        ),
        container="case",
    )


def respond_to_grading_query_form(request, queue_pk, case):
    pv_gradings = get_gov_pv_gradings(request, convert_to_options=True)
    return Form(
        title=PVGradingForm.TITLE,
        description=PVGradingForm.DESCRIPTION,
        questions=[
            Heading(PVGradingForm.HEADING, HeadingStyle.S),
            Summary(
                values={
                    PVGradingForm.Summary.DESCRIPTION: case.data["good"]["description"],
                    PVGradingForm.Summary.PART_NUMBER: default_na(case.data["good"]["part_number"]),
                    PVGradingForm.Summary.IS_THIS_GOOD_CONTROLLED: case.data["good"]["is_good_controlled"]["value"],
                    PVGradingForm.Summary.CONTROL_LIST_ENTRIES: case.data["clc_control_list_entry"],
                    PVGradingForm.Summary.EXPLANATION: case.data["clc_raised_reasons"],
                },
                classes=[
                    "govuk-inset-text",
                    "govuk-summary-list--no-border",
                    "govuk-!-padding-top-0",
                    "govuk-!-padding-bottom-0",
                    "govuk-!-padding-left-6",
                ],
            ),
            Heading(PVGradingForm.YOUR_RESPONSE, HeadingStyle.S),
            Group(
                components=[
                    TextInput(title=PVGradingForm.Grading.PREFIX, name="prefix", optional=True),
                    Select(
                        # request not supplied since static endpoints don't require it.
                        options=pv_gradings,
                        title=PVGradingForm.Grading.GRADING,
                        name="grading",
                    ),
                    TextInput(title=PVGradingForm.Grading.SUFFIX, name="suffix", optional=True),
                ],
                classes=["app-pv-grading-inputs"],
            ),
            DetailComponent(
                title=PVGradingForm.COMMENT,
                components=[
                    TextArea(
                        name="comment",
                        extras={
                            "max_length": 500,
                        },
                    ),
                ],
            ),
        ],
        default_button_name=PVGradingForm.SUBMIT_BUTTON,
        back_link=BackLink(
            url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"]}),
        ),
        container="case",
    )
