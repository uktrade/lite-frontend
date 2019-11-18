from applications.components import back_to_task_list
from core.builtins.custom_tags import get_string
from core.helpers import str_date_only
from lite_forms.components import Form, TextArea, Summary, HiddenField


def confirm_organisation_form(organisation):
    return Form(
        title=get_string("hmrc.confirm_org.title"),
        questions=[
            Summary(
                values={
                    "Name": organisation["name"],
                    "Registration Number": organisation["registration_number"],
                    "EORI Number": organisation["eori_number"],
                    "VAT Number": organisation["vat_number"],
                    "Joined on": str_date_only(organisation["created_at"]),
                }
            ),
            HiddenField("organisation", organisation["id"]),
        ],
        default_button_name=get_string("hmrc.confirm_org.button_text"),
    )


def query_explanation_form(application_id):
    return Form(
        title=get_string("hmrc.query_explanation.title"),
        questions=[TextArea(name="reasoning", optional=True, extras={"max_length": 1000,})],
        default_button_name=get_string("hmrc.query_explanation.button_text"),
        back_link=back_to_task_list(application_id),
    )
