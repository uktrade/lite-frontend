from applications.components import back_to_task_list
from lite_forms.components import Form, RadioButtons, Option, TextInput


def told_by_an_official_form(application_id):
    return Form(
        title="Have you been informed under an end use control that you need to apply for a licence?",
        description="This could be a letter or email from HMRC or another government department.",
        questions=[
            RadioButtons(
                name="have_you_been_informed",
                options=[
                    Option("yes", "Yes", show_pane="pane_reference_number_on_information_form"),
                    Option("no", "No"),
                ],
                classes=["govuk-radios--inline"],
            ),
            TextInput(
                title="Reference number (optional)",
                description="The reference number is on the letter or email.",
                name="reference_number_on_information_form",
                optional=True,
            ),
        ],
        back_link=back_to_task_list(application_id),
    )
