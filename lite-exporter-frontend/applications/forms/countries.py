from applications.components import back_to_task_list
from core.services import get_countries
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, Filter, Checkboxes


def countries_form(application_id):
    return Form(
        title=strings.applications.DestinationForm.TITLE,
        description=strings.applications.DestinationForm.DESCRIPTION,
        questions=[
            Filter(),
            Checkboxes(
                name="countries[]",
                options=get_countries(None, True),
                classes=["govuk-checkboxes--small"],
                show_select_links=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name=strings.SAVE,
        back_link=back_to_task_list(application_id),
    )
