from lite_content.lite_exporter_frontend import strings
from applications.components import back_to_task_list
from core.helpers import str_date_only
from lite_forms.components import Form, TextArea, Summary, HiddenField


def confirm_organisation_form(organisation):
    return Form(
        title=strings.Hmrc.ConfirmOrg.TITLE,
        questions=[
            Summary(
                values={
                    "Name": organisation["name"],
                    "Registration number": organisation["registration_number"],
                    "EORI number": organisation["eori_number"],
                    "VAT number": organisation["vat_number"],
                    "Joined on": str_date_only(organisation["created_at"]),
                }
            ),
            HiddenField("organisation", organisation["id"]),
        ],
        default_button_name=strings.Hmrc.ConfirmOrg.BUTTON_TEXT,
    )


def query_explanation_form(application_id):
    return Form(
        title=strings.Hmrc.QueryExplanation.TITLE,
        questions=[TextArea(name="reasoning", optional=True, extras={"max_length": 1000,})],
        default_button_name=strings.Hmrc.QueryExplanation.BUTTON_TEXT,
        back_link=back_to_task_list(application_id),
    )
