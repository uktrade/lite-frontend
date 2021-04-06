from lite_forms.components import TextInput, AutocompleteInput, TextArea, TokenBar
from lite_forms.helpers import conditional


def country_question(countries, prefix="address."):
    return AutocompleteInput(title="Country", name=prefix + "country", options=countries)


def address_questions(countries, is_commercial, prefix="address."):
    phone_number_label = "Organisation phone number" if is_commercial else "Phone number"
    name = f"{prefix}phone_number"
    return [
        TextInput(title="Building and street", accessible_description="line 1 of 2", name=prefix + "address_line_1",),
        TextInput(title="", accessible_description="line 2 of 2", name=prefix + "address_line_2",),
        TextInput(title="Town or city", name=prefix + "city"),
        TextInput(title="County or state", name=prefix + "region"),
        TextInput(title="Postcode", name=prefix + "postcode"),
        TextInput(title=phone_number_label, name=prefix + "phone_number", description="For international numbers include the country code"),
        TextInput(title="Website address", name=prefix + "website", optional=True),
        conditional(countries, country_question(countries, prefix)),
    ]


def foreign_address_questions(is_commercial, countries, prefix="address."):
    phone_number_label = "Organisation phone number" if is_commercial else "Phone number"
    return [
        TextArea(title="Address", name=prefix + "address", classes=["govuk-input--width-20"], rows=6),
        TextInput(title=phone_number_label, name=prefix + "phone_number", description="For international numbers include the country code"),
        TextInput(title="Website address", name=prefix + "website", optional=True),
        conditional(countries, country_question(countries, prefix)),
    ]


def control_list_entries_question(
    control_list_entries,
    title="Control list entries",
    description="Type to get suggestions. For example, ML1a.",
    name="control_list_entries",
):
    return TokenBar(title=title, name=name, description=description, options=control_list_entries,)


def pv_grading_question(
    pv_gradings, title="PV grading", description="For example, UK OFFICIAL-SENSITIVE", name="pv_grading",
):
    return AutocompleteInput(title=title, name=name, description=description, options=pv_gradings)
