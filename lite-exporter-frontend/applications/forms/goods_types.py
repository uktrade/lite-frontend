from conf.constants import HMRC_QUERY
from core.services import get_control_list_entries
from lite_content.lite_exporter_frontend.goods_types import CreateGoodsTypeForm
from lite_forms.common import control_list_entry_question
from lite_forms.components import TextArea, RadioButtons, Option, Form
from lite_forms.helpers import conditional


def goods_type_form(application_type: str):
    return Form(
        title=CreateGoodsTypeForm.TITLE,
        description=CreateGoodsTypeForm.DESCRIPTION,
        questions=[
            TextArea(title=CreateGoodsTypeForm.Description.TITLE, name="description", extras={"max_length": 2000,}),
            RadioButtons(
                title=CreateGoodsTypeForm.IsControlled.TITLE,
                description=CreateGoodsTypeForm.IsControlled.DESCRIPTION,
                name="is_good_controlled",
                options=[
                    Option(key="yes", value=CreateGoodsTypeForm.IsControlled.YES, show_pane="pane_control_code"),
                    Option(key="no", value=CreateGoodsTypeForm.IsControlled.NO),
                ],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                name="control_code",
                inset_text=False,
            ),
            conditional(
                application_type != HMRC_QUERY,
                RadioButtons(
                    title=CreateGoodsTypeForm.IsIncorporated.TITLE,
                    description=CreateGoodsTypeForm.IsIncorporated.DESCRIPTION,
                    name="is_good_incorporated",
                    options=[
                        Option(key=True, value=CreateGoodsTypeForm.IsIncorporated.YES),
                        Option(key=False, value=CreateGoodsTypeForm.IsIncorporated.NO),
                    ],
                    classes=["govuk-radios--inline"],
                ),
            ),
        ],
    )
