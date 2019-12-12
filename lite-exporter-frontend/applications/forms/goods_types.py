from core.builtins.custom_tags import get_string
from lite_forms.common import control_list_entry_question
from lite_forms.components import TextArea, RadioButtons, Option, Form

from core.services import get_control_list_entries


def goods_type_form():
    return Form(
        title=get_string("good_types.overview.title"),
        questions=[
            TextArea(title="Description", name="description", extras={"max_length": 2000,}),
            RadioButtons(
                title="Are your products controlled?",
                description="Products that aren't on the <a class='govuk-link' target='_blank' "
                "href='https://permissions-finder.service.trade.gov.uk/'>control list</a> "
                "may be affected by military end use controls, current trade sanctions and embargoes or weapons of "
                "mass destruction controls. If your products aren't subject to any controls, you'll get a no licence "
                "required (NLR) document from ECJU.",
                name="is_good_controlled",
                options=[Option(key="yes", value="Yes", show_pane="pane_control_code"), Option(key="no", value="No")],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title="Control list classification",
                description="For example, ML1a.",
                name="control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Will the products be incorporated into other products",
                description="",
                name="is_good_end_product",
                options=[Option(key="yes", value="Yes"), Option(key="no", value="No")],
                classes=["govuk-radios--inline"],
            ),
        ],
    )
