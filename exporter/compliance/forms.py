from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend.compliance import OpenReturnsForm, OpenReturnsHelpPage
from lite_forms.components import FormGroup, Form, Select, Option, FileUpload, Label, DetailComponent, BackLink, Custom
from django.utils import timezone


def get_years():
    current_year = timezone.localtime().year
    previous_year = current_year - 1
    return [Option(key=current_year, value=current_year), Option(key=previous_year, value=previous_year)]


def open_licence_return_form_group():
    FORMATTING_HELP_DETAILS = """
    The first row must contain column headers, or be blank. It must not contain returns data.<br>Columns must start from column A and be in the following order:<br><ul>
        <li>Licence number</li>
        <li>Destination</li>
        <li>End user type</li>
        <li>Usage count</li>
        <li>Period</li>
        </ul><br>Licence number must be in one of the following formats:<br><ul>
        <li>GBOXX20XX/XXXXX. For example GBOIE2020/00001)</li>
        <li>GBOXX20XX/XXXXX/X for amended licences. For example GBOIE2020/00001/A</li>
        </ul><br>Destination names must be entered exactly as they appear on the licence.<br><br>End user type must be one of the following, entered exactly as shown here:<br><ul>
        <li>Government</li>
        <li>Commercial</li>
        <li>Pvt Indiv</li>
        <li>Other</li>
        </ul><br>Usage count must be a positive integer.<br><br>Period must be in the following format, entered exactly as shown with YY replaced with the last 2 digits of the year:<br><ul>
        <li>01-JAN-YY to 31-DEC-YY</li>
        </ul>
    """
    return FormGroup(
        [
            Form(
                title=OpenReturnsHelpPage.TITLE,
                questions=[
                    Label(OpenReturnsHelpPage.DESCRIPTION),
                    DetailComponent("Format your open licence returns CSV", FORMATTING_HELP_DETAILS),
                ],
                default_button_name=OpenReturnsHelpPage.BUTTON,
                back_link=BackLink(OpenReturnsHelpPage.BACK, reverse_lazy("core:home")),
            ),
            Form(
                title=OpenReturnsForm.Year.TITLE,
                description="",
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
                description="The file must be smaller than 1MB",
                questions=[
                    FileUpload(),
                    Label("<h2>Your file needs to look like the following example</h2>Save your file as a CSV"),
                    Custom("components/spreadsheet.html"),
                ],
                default_button_name=OpenReturnsForm.Upload.BUTTON,
            ),
        ]
    )
