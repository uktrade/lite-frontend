from lite_content.lite_internal_frontend import strings
from lite_forms.common import address_questions
from lite_forms.components import (
    Form,
    TextInput,
    Heading,
    HelpSection,
    FormGroup,
    Option,
    RadioButtons,
    HiddenField,
)
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle

from core.builtins.custom_tags import get_string
from core.services import get_countries


def register_business_forms(individual=False, name=""):
    return FormGroup(
        [
            Form(
                title=get_string("register_business.commercial_or_private_individual"),
                questions=[
                    RadioButtons(
                        name="type",
                        options=[
                            Option(key="commercial", value="Commercial"),
                            Option(key="individual", value="Individual"),
                        ],
                    )
                ],
                default_button_name=strings.CONTINUE,
            ),
            conditional(
                individual,
                Form(
                    title=get_string("register_business.register_individual_title"),
                    questions=[
                        TextInput(title=strings.REGISTER_BUSINESS_FIRST_AND_LAST_NAME, name="name"),
                        TextInput(title=get_string("register_business.email"), name="user.email"),
                        TextInput(title=get_string("register_business.eori_number"), name="eori_number"),
                        TextInput(
                            title=get_string("register_business.uk_vat_number.title"),
                            description=get_string("register_business.uk_vat_number.description"),
                            optional=True,
                            name="vat_number",
                        ),
                    ],
                    default_button_name=strings.CONTINUE,
                ),
                Form(
                    title=get_string("register_business.register_commercial_title"),
                    questions=[
                        TextInput(title=get_string("register_business.name"), name="name"),
                        TextInput(title=get_string("register_business.eori_number"), name="eori_number"),
                        TextInput(
                            title=get_string("register_business.sic_number"),
                            description="Classifies industries by a four-digit code.",
                            name="sic_number",
                        ),
                        TextInput(
                            title=get_string("register_business.uk_vat_number.title"),
                            description=get_string("register_business.uk_vat_number.description"),
                            name="vat_number",
                        ),
                        TextInput(
                            title=get_string("register_business.crn"),
                            description=get_string("register_business.crn_description"),
                            name="registration_number",
                        ),
                    ],
                    default_button_name=strings.CONTINUE,
                ),
            ),
            Form(
                title=get_string("register_business.create_default_site"),
                questions=[
                    TextInput(title=get_string("register_business.name_of_site"), name="site.name"),
                    Heading(get_string("register_business.where_is_the_exporter_based"), HeadingStyle.M),
                    *address_questions(get_countries(None, True), "site.address."),
                ],
                default_button_name=strings.CONTINUE,
            ),
            conditional(
                not individual,
                Form(
                    title="Create an admin user for " + name,
                    questions=[TextInput(title=get_string("register_business.email"), name="user.email"),],
                    default_button_name="Submit",
                    helpers=[HelpSection("Help", get_string("register_business.default_user"))],
                ),
            ),
        ],
        show_progress_indicators=True,
    )


def register_hmrc_organisation_forms(name=""):
    return FormGroup(
        [
            Form(
                title="Register an HMRC organisation",
                questions=[
                    HiddenField(name="type", value="hmrc"),
                    TextInput(title="Name of HMRC organisation", name="name"),
                    TextInput(title=get_string("register_business.name_of_site"), name="site.name"),
                    Heading("Where are they based?", HeadingStyle.M),
                    *address_questions(get_countries(None, True), "site.address."),
                ],
                default_button_name="Continue",
            ),
            Form(
                title="Create an admin for " + name,
                questions=[TextInput(title=get_string("register_business.email"), name="user.email"),],
                default_button_name="Submit",
                helpers=[HelpSection("Help", get_string("register_business.default_user"))],
            ),
        ],
        show_progress_indicators=True,
    )
