from core.builtins.custom_tags import get_string
from lite_forms.common import control_list_entry_question
from lite_forms.components import TextArea, RadioButtons, Option, Form

from core.services import get_control_list_entries


def goods_type_form():
    return Form(
        title=get_string("good_types.overview.title"),
        questions=[
            TextArea(title="Give a short description of your goods.", name="description", extras={"max_length": 280,}),
            RadioButtons(
                title="Is your good controlled?",
                description='If you don\'t know you can use <a class="govuk-link" target="_blank" '
                'href="https://permissions-finder.service.trade.gov.uk/">Permissions Finder</a>.',
                name="is_good_controlled",
                options=[Option(key="yes", value="Yes", show_pane="pane_control_code"), Option(key="no", value="No")],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title="What's your good's control list entry?",
                description="For example, ML1a.",
                name="control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Is your good intended to be incorporated into an end product?",
                description="",
                name="is_good_end_product",
                options=[Option(key="yes", value="Yes"), Option(key="no", value="No")],
                classes=["govuk-radios--inline"],
            ),
        ],
    )
