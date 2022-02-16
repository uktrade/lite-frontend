from django import forms

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
                options=[
                    Option(key=True, value="Yes"),
                    Option(key=False, value="No"),
                ],
            ),
            control_list_entries_question(
                control_list_entries=control_list_entries,
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


class ExportControlCharacteristicsForm(forms.Form):

    MESSAGE_NO_CLC_MUTEX = "This is mutually exclusive with Control list entries"
    MESSAGE_NO_CLC_REQUIRED = "Select a control list entry or select 'This product does not have a control list entry'"

    control_list_entries = forms.MultipleChoiceField(
        label="What is the correct control list entry for this product?",
        help_text="Type to get suggestions. For example ML1a.",
        choices=[],  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_list_entries"}),
    )
    does_not_have_control_list_entries = forms.BooleanField(
        label="This product does not have a control list entry",
        required=False,
    )
    is_precedent = forms.BooleanField(label="Mark this product rating as a precedent", required=False)
    is_good_controlled = forms.TypedChoiceField(
        label="Is a licence required?",
        coerce=lambda x: x == "True",
        choices=[
            (True, "Yes"),
            (False, "No"),
        ],
        widget=forms.RadioSelect,
        required=False,
    )
    end_use_control = forms.MultipleChoiceField(
        label="What is the end use control rating for this product?",
        help_text="Type to get suggestions. For example MEND.",
        choices=[
            ("MEND", "MEND"),
            ("END", "END"),
            ("ENDTA", "ENDTA"),
            ("MEND1", "MEND1"),
        ],
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_rating"}),
    )
    report_summary = forms.CharField(
        label="Select an annual report summary",
        help_text="Type to get suggestions. For example, components for body armour.",
        # setting id for javascript to use
        widget=forms.TextInput(attrs={"id": "report_summary"}),
    )
    comment = forms.CharField(
        label="Comment (optional)",
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, control_list_entries_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control_list_entries"].choices = control_list_entries_choices

    def clean(self):
        cleaned_data = super().clean()
        has_none = cleaned_data["does_not_have_control_list_entries"]
        has_some = bool(cleaned_data["control_list_entries"])
        if has_none and has_some:
            raise forms.ValidationError({"does_not_have_control_list_entries": self.MESSAGE_NO_CLC_MUTEX})
        elif not has_none and not has_some:
            raise forms.ValidationError({"does_not_have_control_list_entries": self.MESSAGE_NO_CLC_REQUIRED})
        return cleaned_data
