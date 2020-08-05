from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend.compliance import OpenReturnsForm, OpenReturnsHelpPage
from lite_forms.components import FormGroup, Form, Select, Option, FileUpload, Label, DetailComponent, BackLink, Custom
from datetime import datetime


def get_years():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return [Option(key=current_year, value=current_year), Option(key=previous_year, value=previous_year)]


def open_licence_return_form_group():
    return FormGroup(
        [
            Form(
                title=OpenReturnsHelpPage.TITLE,
                questions=[
                    Label(OpenReturnsHelpPage.DESCRIPTION),
                    DetailComponent(
                        OpenReturnsHelpPage.FORMATTING_HELP_LINK, OpenReturnsHelpPage.FORMATTING_HELP_DETAILS
                    ),
                ],
                default_button_name=OpenReturnsHelpPage.BUTTON,
                back_link=BackLink(OpenReturnsHelpPage.BACK, reverse_lazy("core:home")),
            ),
            Form(
                title=OpenReturnsForm.Year.TITLE,
                description=OpenReturnsForm.Year.DESCRIPTION,
                questions=[
                    Select(
                        title=OpenReturnsForm.Year.FIELD_TITLE,
                        description=OpenReturnsForm.Year.FIELD_DESCRIPTION,
                        name="year",
                        options=get_years(),
                    )
                ],
                default_button_name=OpenReturnsForm.Year.BUTTON,
            ),
            Form(
                title=OpenReturnsForm.Upload.TITLE,
                description=OpenReturnsForm.Upload.DESCRIPTION,
                questions=[
                    FileUpload(),
                    Label(OpenReturnsForm.Upload.ExampleTable.HEADING),
                    Custom("components/spreadsheet.html"),
                ],
                default_button_name=OpenReturnsForm.Upload.BUTTON,
            ),
        ]
    )
