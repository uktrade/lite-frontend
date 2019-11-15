from django.template.defaultfilters import default
from django.urls import reverse_lazy
from lite_forms.common import control_list_entry_question
from lite_forms.components import Form, BackLink, RadioButtons, Option, TextArea, HTMLBlock, Heading, HiddenField
from lite_forms.styles import HeadingStyle

from core.builtins.custom_tags import reference_code
from core.services import get_control_list_entries
from picklists.services import get_picklists


def respond_to_clc_query_form(request, case):
    return Form(
        title="Respond to CLC Query",
        questions=[
            Heading(reference_code(case["query"]["id"]), HeadingStyle.S),
            HTMLBlock(
                html='<div class="app-summary-list app-inset-text">'
                '<div class="app-summary-list__item">'
                '<p class="govuk-caption-m">Description</p>'
                '<p class="govuk-body-m">' + case["query"]["good"]["description"] + "</p>"
                "</div>"
                '<div class="app-summary-list__item">'
                '<p class="govuk-caption-m">Control list entry</p>'
                '<p class="govuk-body-m">' + default(case["query"]["good"].get("control_code"), "N/A") + "</p>"
                "</div>"
                "</div>"
            ),
            HTMLBlock(html='<hr class="lite-horizontal-separator">'),
            RadioButtons(
                title="Is this good controlled?",
                name="is_good_controlled",
                options=[Option(key="yes", value="Yes", show_pane="pane_control_code"), Option(key="no", value="No")],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title="What is the correct control list entry?",
                name="control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Which report summary would you like to use? (optional)",
                name="report_summary",
                options=get_picklists(request, "report_summary", convert_to_options=True, include_none=True),
                description="You only need to do this if the item is controlled",
                classes=["test"],
            ),
            TextArea(title="Good's comment (optional)", name="comment", optional=True, extras={"max_length": 500,}),
            HiddenField("validate_only", True),
        ],
        default_button_name="Continue to overview",
        back_link=BackLink("Back to case", reverse_lazy("cases:case", kwargs={"pk": case["id"]})),
    )
