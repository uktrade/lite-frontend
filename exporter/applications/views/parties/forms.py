from core.common.forms import BaseForm
from django import forms


class ConsigneeTypeForm(BaseForm):
    class Layout:
        TITLE = "What is the Consignee type?"

    consignee_type = forms.CharField(
        widget=forms.TextInput,
        label="",
        error_messages={
            "required": " Enter the Consignee type",
        },
    )

    def get_layout_fields(self):
        return ("consignee_type",)


class ConsigneeNameForm(BaseForm):
    class Layout:
        TITLE = "What is the Consignee name?"

    consignee_name = forms.CharField(
        widget=forms.TextInput,
        label="",
        error_messages={
            "required": " Enter the Consignee name",
        },
    )

    def get_layout_fields(self):
        return ("consignee_name",)


class ConsigneeAddressForm(BaseForm):
    class Layout:
        TITLE = "What is the Consignee address?"

    consignee_address = forms.CharField(
        widget=forms.TextInput,
        label="",
        error_messages={
            "required": " Enter the Consignee address",
        },
    )

    def get_layout_fields(self):
        return ("consignee_address",)
