from django import forms

from core.common.forms import BaseForm


class ApplicationNameForm(BaseForm):
    class Layout:
        TITLE = "Name of the application"
        TITLE_AS_LABEL_FOR = "name"
        SUBMIT_BUTTON_TEXT = "Continue"

    name = forms.CharField(
        label="",
        help_text="Give the application a reference name so you can refer back to it when needed",
    )

    def get_layout_fields(self):
        return ("name",)


class ApplicationPreviousApplicationForm(BaseForm):
    class Layout:
        TITLE = "Have you made a previous application?"
        TITLE_AS_LABEL_FOR = "previous_application"
        SUBMIT_BUTTON_TEXT = "Save"

    previous_application = forms.ChoiceField(
        label="",
        help_text="Some help text",
        widget=forms.RadioSelect,
        choices=(
            ("Yes", "Yes"),
            ("No", "No"),
        ),
    )

    def get_layout_fields(self):
        return ("previous_application",)


class ApplicationSubmissionForm(BaseForm):
    class Layout:
        TITLE = ""
        SUBMIT_BUTTON_TEXT = "Submit"

    def get_layout_fields(self):
        return []


class ProductNameAndDescriptionForm(BaseForm):
    class Layout:
        TITLE = "Add a product"
        SUBMIT_BUTTON_TEXT = "Continue"

    name = forms.CharField(
        label="Give the product a descriptive name",
        help_text="Try to match the name as closely as possible to any documentation, like the technical specification",
    )
    description = forms.CharField(
        label="Description",
        help_text="Provide a description of the product you are seeking approval to release. Include any detailed technical specifications.",
        widget=forms.Textarea(),
    )

    def get_layout_fields(self):
        return ("name", "description")


class EndUserNameForm(BaseForm):
    party_type = "John"
    party_type_readable = party_type.replace("_", " ")
    title = f"Name of the {party_type_readable}"
    help_text = f"Give the {party_type_readable} a name"

    party_name_field = forms.CharField(
        label="",
        help_text=help_text,
    )

    class Layout:
        SUBMIT_BUTTON_TEXT = "Continue"

    def get_title(self):
        return self.title

    def get_field_label(self, field_name):
        return super().get_field_label(field_name)

    def get_layout_fields(self):
        return ("party_name_field",)


# class PartyNameForm(BaseForm):
#     class Layout():
#         party_type = "party"
#         party_type_var = party_type.replace(" ", "_")
#         TITLE = f"Name of the {party_type}"
#         TITLE_AS_LABEL_FOR = f"{party_type_var}_name"
#         SUBMIT_BUTTON_TEXT = "Continue"

#     layout_field_name = Layout.party_type.replace(" ", "_") + "_name"
#     str(layout_field_name) = forms.CharField(
#         label="",
#         help_text=f"Give the name of the {Layout.party_type}",
#     )

#     def get_layout_fields(self):
#         return (self.layout_field_name,)


# class EndUserNameForm(PartyNameForm):
#     party_type = "end user"
#     class Layout:
#         party_type = "end user"
#         party_type_var = party_type.replace(" ", "_")
#         TITLE = f"Name of the {party_type}"
#         TITLE_AS_LABEL_FOR = f"{party_type_var}_name"
#         SUBMIT_BUTTON_TEXT = "Continue"
