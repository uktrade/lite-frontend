from lite_forms.components import RadioButtons, Option, Form

from core.helpers import str_date_only


def select_your_organisation_form(organisations):
    return Form(
        "Select an organisation",
        "You can switch between organisations from your dashboard.",
        [
            RadioButtons(
                name="organisation",
                options=[
                    Option(x["id"], x["name"], "Member since " + str_date_only(x["joined_at"])) for x in organisations
                ],
            )
        ],
        default_button_name="Save and continue",
        back_link=None,
    )
