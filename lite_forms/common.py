from lite_forms.components import Form, Heading, TextInput, AutocompleteInput, TextArea, TokenBar
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle
from lite_content.lite_internal_frontend.organisations import RegisterAnOrganisation


def country_question(countries, prefix="address."):
    return AutocompleteInput(title="Country", name=prefix + "country", options=countries)


def address_questions(countries, is_individual, prefix="address."):
    phone_number_title = "Phone number" if is_individual else "Organisation phone number"
    return [
        TextInput(
            title="Building and street",
            accessible_description="line 1 of 2",
            name=prefix + "address_line_1",
        ),
        TextInput(
            title="",
            accessible_description="line 2 of 2",
            name=prefix + "address_line_2",
        ),
        TextInput(title="Town or city", name=prefix + "city"),
        TextInput(title="County or state", name=prefix + "region"),
        TextInput(title="Postcode", name=prefix + "postcode"),
        TextInput(
            title=phone_number_title,
            name="phone_number",
            description="For international numbers include the country code",
        ),
        TextInput(title="Website", name="website"),
        conditional(countries, country_question(countries, prefix)),
    ]


def foreign_address_questions(is_individual, countries, prefix="address."):
    phone_number_title = "Phone number" if is_individual else "Organisation phone number"
    return [
        TextArea(title="Address", name=prefix + "address", classes=["govuk-input--width-20"], rows=6),
        TextInput(
            title=phone_number_title,
            name="phone_number",
            description="For international numbers include the country code",
        ),
        TextInput(title="Website", name="website"),
        conditional(countries, country_question(countries, prefix)),
    ]


def edit_address_questions_form(is_commercial, in_uk, countries, prefix="site.address."):
    phone_number_label = "Organisation phone number" if is_commercial else "Phone number"

    if in_uk:
        questions = [
            TextInput(title=RegisterAnOrganisation.NAME_OF_SITE, name="site.name"),
            Heading(RegisterAnOrganisation.WhereIsTheExporterBased.TITLE, HeadingStyle.M),
            TextInput(
                title="Building and street",
                accessible_description="line 1 of 2",
                name=prefix + "address_line_1",
            ),
            TextInput(
                title="",
                accessible_description="line 2 of 2",
                name=prefix + "address_line_2",
            ),
            TextInput(title="Town or city", name=prefix + "city"),
            TextInput(title="County or state", name=prefix + "region"),
            TextInput(title="Postcode", name=prefix + "postcode"),
        ]
    else:
        questions = [
            TextInput(title=RegisterAnOrganisation.NAME_OF_SITE, name="site.name"),
            Heading(RegisterAnOrganisation.WhereIsTheExporterBased.TITLE, HeadingStyle.M),
            TextArea(title="Address", name=prefix + "address", classes=["govuk-input--width-20"], rows=6),
        ]

    return Form(
        title="Edit default site for this exporter",
        questions=questions
        + [
            TextInput(
                title=phone_number_label,
                name="phone_number",
                description="For international numbers include the country code",
            ),
            TextInput(title="Website", name="website", optional=True),
            conditional(not in_uk, AutocompleteInput(title="Country", name=prefix + "country", options=countries)),
        ],
    )


def control_list_entries_question(
    control_list_entries,
    title="Control list entries",
    description="Type to get suggestions. For example, ML1a.",
    name="control_list_entries",
):
    return TokenBar(
        title=title,
        name=name,
        description=description,
        options=control_list_entries,
    )


def pv_grading_question(
    pv_gradings,
    title="PV grading",
    description="For example, UK OFFICIAL-SENSITIVE",
    name="pv_grading",
):
    return AutocompleteInput(title=title, name=name, description=description, options=pv_gradings)
