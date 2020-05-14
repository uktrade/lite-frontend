from django.urls import reverse_lazy

from core.builtins.custom_tags import default_na
from core.services import get_control_list_entries, get_gov_pv_gradings
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
from picklists.services import get_picklists_for_input


def respond_to_clc_query_form(request, queue_pk, case):
    return Form(
        title=CLCReviewGoods.TITLE,
        description=CLCReviewGoods.DESCRIPTION,
        questions=[
            Heading(CLCReviewGoods.HEADING, HeadingStyle.S),
            Summary(
                values={
                    CLCReviewGoods.Summary.DESCRIPTION: case["query"]["good"]["description"],
                    CLCReviewGoods.Summary.PART_NUMBER: default_na(case["query"]["good"]["part_number"]),
                    CLCReviewGoods.Summary.IS_THIS_GOOD_CONTROLLED: case["query"]["good"]["is_good_controlled"][
                        "value"
                    ],
                    CLCReviewGoods.Summary.CONTROL_LIST_ENTRIES: case["query"]["clc_control_list_entry"],
                    CLCReviewGoods.Summary.EXPLANATION: case["query"]["clc_raised_reasons"],
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
                        key="yes",
                        value=CLCReviewGoods.Controlled.YES,
                        components=[
                            control_list_entries_question(
                                control_list_entries=get_control_list_entries(request, convert_to_options=True),
                                title=CLCReviewGoods.CONTROL_LIST_ENTRY,
                            ),
                            RadioButtons(
                                title=CLCReviewGoods.ReportSummary.TITLE,
                                name="report_summary",
                                options=get_picklists_for_input(request, "report_summary", convert_to_options=True),
                            ),
                        ],
                    ),
                    Option(key="no", value=CLCReviewGoods.Controlled.NO),
                ],
            ),
            DetailComponent(
                title=CLCReviewGoods.COMMENT, components=[TextArea(name="comment", extras={"max_length": 500,}),],
            ),
        ],
        default_button_name=CLCReviewGoods.SUBMIT_BUTTON,
        back_link=BackLink(url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"]}),),
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
                    PVGradingForm.Summary.DESCRIPTION: case["query"]["good"]["description"],
                    PVGradingForm.Summary.PART_NUMBER: default_na(case["query"]["good"]["part_number"]),
                    PVGradingForm.Summary.IS_THIS_GOOD_CONTROLLED: case["query"]["good"]["is_good_controlled"]["value"],
                    PVGradingForm.Summary.CONTROL_LIST_ENTRIES: case["query"]["clc_control_list_entry"],
                    PVGradingForm.Summary.EXPLANATION: case["query"]["clc_raised_reasons"],
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
                title=PVGradingForm.COMMENT, components=[TextArea(name="comment", extras={"max_length": 500,}),],
            ),
        ],
        default_button_name=PVGradingForm.SUBMIT_BUTTON,
        back_link=BackLink(url=reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"]}),),
        container="case",
    )
