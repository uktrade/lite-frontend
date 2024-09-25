from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.flags import SetFlagsForm
from lite_forms.components import (
    Option,
    Form,
    DetailComponent,
    TextArea,
    Checkboxes,
    HelpSection,
    Filter,
)

level_options = [
    Option("Case", "Case"),
    Option("Organisation", "Organisation"),
    Option("Destination", "Destination"),
    Option("Good", "Good"),
]


_levels = [
    Option(key="Good", value=strings.FlaggingRules.Create.Type.GOOD),
    Option(key="Destination", value=strings.FlaggingRules.Create.Type.DESTINATION),
    Option(key="Case", value=strings.FlaggingRules.Create.Type.APPLICATION),
]


def set_flags_form(flags, level, show_case_header=False, show_sidebar=False):
    form = Form(
        title=getattr(SetFlagsForm, level).TITLE,
        description=getattr(SetFlagsForm, level).DESCRIPTION,
        questions=[
            Filter(placeholder=getattr(SetFlagsForm, level).FILTER),
            Checkboxes(
                name="flags[]",
                options=flags,
                filterable=True,
                disabled_hint="You do not have permission to remove this flag.",
            ),
            DetailComponent(
                title=getattr(SetFlagsForm, level).Note.TITLE,
                components=[
                    TextArea(name="note", classes=["govuk-!-margin-0"]),
                ],
            ),
        ],
        default_button_name=getattr(SetFlagsForm, level).SUBMIT_BUTTON,
        container="case" if show_case_header else "two-pane",
        javascript_imports={"/javascripts/flags-permission-hints.js"},
    )

    if show_sidebar:
        form.helpers = [HelpSection("Setting flags on:", "", includes="case/includes/selection-sidebar.html")]

    return form
