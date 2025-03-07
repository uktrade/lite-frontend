from django import forms
from crispy_forms_gds.choices import Choice

from core.common.forms import BaseForm
from core.forms.layouts import F680ConditionalCheckboxes, F680ConditionalCheckboxesQuestion


class EntityTypeForm(BaseForm):
    class Layout:
        TITLE = "Select type of entity"
        TITLE_AS_LABEL_FOR = "entity_type"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    entity_type = forms.ChoiceField(
        choices=(
            Choice(
                "end-user",
                "End user",
                hint=(
                    "An end-user receives the products in the destination country. They either "
                    "use the products themselves, resell from stock, or export them again to another country."
                ),
            ),
            Choice(
                "ultimate-end-user",
                "Ultimate end-user",
                hint=(
                    "Ultimate end-users receive products or information from end-users. They can "
                    "be the same products or information that you shared with the end-user. Or the "
                    "end-user can change the products or information before sharing them with the ultimate end-user."
                ),
            ),
            Choice(
                "third-party",
                "Third party",
                hint=(
                    "A third party is involved in sharing products or information, but "
                    "doesn't use them. They are not an end-user or ultimate end-user. They may be an agent, "
                    "broker, consultant or distributor."
                ),
            ),
        ),
        label="Select type of entity",
        widget=forms.RadioSelect,
    )

    def get_layout_fields(self):
        return ("entity_type",)


class ThirdPartyRoleForm(BaseForm):
    class Layout:
        TITLE = "Select the role of the third party"
        TITLE_AS_LABEL_FOR = "third_party_role"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    third_party_role = forms.ChoiceField(
        choices=(
            Choice(
                "agent-or-broker",
                "Agent or broker",
            ),
            Choice(
                "intermediate-consignee",
                "Intermediate consignee",
            ),
            Choice(
                "authorised-submitter",
                "Authorised submitter",
            ),
            Choice(
                "consultant",
                "Consultant",
            ),
            Choice(
                "contact",
                "Contact",
            ),
            Choice(
                "exporter",
                "Exporter",
            ),
            Choice(
                "other",
                "Other",
            ),
        ),
        label=Layout.TITLE,
        widget=forms.RadioSelect,
    )

    def get_layout_fields(self):
        return ("third_party_role",)


class EndUserNameForm(BaseForm):
    class Layout:
        TITLE = "End-user name"
        TITLE_AS_LABEL_FOR = "end_user_name"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    end_user_name = forms.CharField(
        label="End-user name",
        help_text="Name or organisation or individual",
    )

    def get_layout_fields(self):
        return ("end_user_name",)


class EndUserAddressForm(BaseForm):
    class Layout:
        TITLE = "End-user address"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    address = forms.CharField(
        label="Address",
        widget=forms.Textarea(attrs={"rows": "5"}),
    )
    country = forms.ChoiceField(
        label="Country",
        choices=[],
        widget=forms.widgets.Select(attrs={"data-module": "autocomplete-select"}),
    )

    def __init__(self, *args, countries=None, **kwargs):
        super().__init__(*args, **kwargs)
        country_choices = [("", "")] + [(country["id"], country["name"]) for country in countries]
        self.fields["country"].choices = country_choices

    def get_layout_fields(self):
        return ("address", "country")


class SecurityGradingForm(BaseForm):
    class Layout:
        TITLE = "What is the security grading of the information or products you want to release to this entity"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    prefix = forms.CharField(
        label="Enter a prefix (optional)",
        required=False,
    )
    security_classification = forms.ChoiceField(
        choices=(
            Choice("official", "Official"),
            Choice("official-sensitive", "Official-Sensitive"),
            Choice("secret", "Secret"),
            Choice("top-secret", "Top Secret", divider="Or"),
            Choice("other", "Other"),
        ),
        label="Select security classification",
        widget=forms.RadioSelect,
    )
    suffix = forms.CharField(
        label="Enter a suffix (optional)",
        required=False,
    )

    def get_layout_fields(self):
        return (
            "prefix",
            "security_classification",
            "suffix",
        )


class EndUserIntendedEndUseForm(BaseForm):
    class Layout:
        TITLE = "How does the end-user intend to use this product"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    end_user_intended_end_use = forms.CharField(
        label="How does the end-user intend to use this product",
        widget=forms.Textarea(attrs={"rows": "5"}),
        help_text="Include as much information as you can. We need to know if they will integrate it into other equipment, involve any third parties, etc.",
    )

    def get_layout_fields(self):
        return ("end_user_intended_end_use",)


class EndUserAssembleManufactureForm(BaseForm):
    class Layout:
        TITLE = "Does this end-user need to assemble or manufacture any of the products?"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    assemble_manufacture_choices = (
        Choice("assemble", "Yes, assembled"),
        Choice("manufacture", "Yes, manufactured"),
        Choice("no", "No"),
    )

    assemble_manufacture = forms.MultipleChoiceField(
        choices=assemble_manufacture_choices,
        label=Layout.TITLE,
    )
    assemble = forms.CharField(
        label="Describe what assembly is needed.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )
    manufacture = forms.CharField(
        label="Describe what manufacture is needed. Be sure to include the manufacturer's website if they have one.",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    def __init__(self, *args, **kwargs):
        self.conditional_checkbox_choices = (
            F680ConditionalCheckboxesQuestion(choices.label, choices.value)
            for choices in self.assemble_manufacture_choices
        )
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return (F680ConditionalCheckboxes("assemble_manufacture", *self.conditional_checkbox_choices),)
