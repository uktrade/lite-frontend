from django.urls import reverse
from django.utils.html import mark_safe

from caseworker.core.components import PicklistPicker
from caseworker.core.services import get_control_list_entries
from lite_content.lite_internal_frontend import goods
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.common import control_list_entries_question
from lite_forms.components import Form, RadioButtons, Option, TextArea, DetailComponent, HelpSection, BackLink
from caseworker.picklists.enums import PicklistCategories


def review_goods_form(request, is_goods_type, **kwargs):
    if is_goods_type:
        comment_components = [TextArea(name="comment", extras={"max_length": 500})]
    else:
        comment_components = [
            TextArea(
                title=mark_safe("Comment about the product <b>in the context of this specific application</b>"),
                description="This information will be attached to the application",
                name="comment",
                extras={"max_length": 500},
            ),
            TextArea(
                title=mark_safe("Comment about the product <b>independent of this application</b>"),
                description="This information will be attached to the product",
                name="canonical_good_comment",
                extras={"max_length": 500},
            ),
        ]

    return Form(
        title=cases.ReviewGoodsForm.HEADING,
        questions=[
            RadioButtons(
                title=goods.ReviewGoods.IS_GOOD_CONTROLLED,
                name="is_good_controlled",
                options=[Option(key=True, value="Yes"), Option(key=False, value="No"),],
            ),
            control_list_entries_question(
                control_list_entries=get_control_list_entries(request, convert_to_options=True),
                title=goods.ReviewGoods.ControlListEntries.TITLE,
            ),
            PicklistPicker(
                target="report_summary",
                title=goods.ReviewGoods.ReportSummary.TITLE,
                description=goods.ReviewGoods.ReportSummary.DESCRIPTION,
                type=PicklistCategories.report_summary.key,
                set_text=False,
                allow_clear=True,
            ),
            DetailComponent(title=goods.ReviewGoods.Comment.TITLE, components=comment_components,),
        ],
        default_button_name=cases.ReviewGoodsForm.CONFIRM_BUTTON,
        container="case",
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]})),
        helpers=[HelpSection(goods.ReviewGoods.GIVING_ADVICE_ON, "", includes="case/includes/selection-sidebar.html")],
    )
