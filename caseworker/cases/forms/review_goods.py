from caseworker.core.components import PicklistPicker
from lite_content.lite_internal_frontend import goods
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.common import control_list_entries_question
from lite_forms.components import Form, RadioButtons, Option, TextArea, DetailComponent, HelpSection, BackLink
from caseworker.picklists.enums import PicklistCategories


def review_goods_form(control_list_entries, back_url):
    return Form(
        title=cases.ReviewGoodsForm.HEADING,
        questions=[
            RadioButtons(
                title=goods.ReviewGoods.IS_GOOD_CONTROLLED,
                name="is_good_controlled",
                options=[Option(key=True, value="Yes"), Option(key=False, value="No"),],
            ),
            control_list_entries_question(
                control_list_entries=control_list_entries, title=goods.ReviewGoods.ControlListEntries.TITLE,
            ),
            PicklistPicker(
                target="report_summary",
                title=goods.ReviewGoods.ReportSummary.TITLE,
                description=goods.ReviewGoods.ReportSummary.DESCRIPTION,
                type=PicklistCategories.report_summary.key,
                set_text=False,
                allow_clear=True,
            ),
            DetailComponent(
                title=goods.ReviewGoods.Comment.TITLE,
                components=[TextArea(name="comment", extras={"max_length": 500})],
            ),
        ],
        default_button_name=cases.ReviewGoodsForm.CONFIRM_BUTTON,
        container="case",
        back_link=BackLink(url=back_url),
        helpers=[HelpSection(goods.ReviewGoods.GIVING_ADVICE_ON, "", includes="case/includes/selection-sidebar.html")],
    )
