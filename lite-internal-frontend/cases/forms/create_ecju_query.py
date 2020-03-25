from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import Form, BackLink, TextArea, HiddenField, RadioButtons
from lite_forms.generators import confirm_form


def choose_picklist_type_form(options, case_url):
    return Form(
        title=cases.EcjuQueries.AddQuery.CHOOSE_TYPE,
        questions=[RadioButtons(name="ecju_query_type", options=options)],
        back_link=BackLink("Back to " + cases.EcjuQueries.TITLE, case_url),
    )


def choose_ecju_query_type_form(case_url, picklists):
    return Form(
        title=cases.EcjuQueries.AddQuery.DROPDOWN_TITLE,
        questions=[
            RadioButtons(
                description=cases.EcjuQueries.AddQuery.DROPDOWN_DESCRIPTION, name="picklist", options=picklists,
            ),
            HiddenField(name="form_name", value="ecju_query_type_select"),
        ],
        back_link=BackLink("Back to " + cases.EcjuQueries.BACK_TO_CHOOSE_TYPE_FORM, case_url),
        default_button_name="Continue",
    )


def create_ecju_query_write_or_edit_form(choose_picklist_url):
    return Form(
        title=cases.EcjuQueries.AddQuery.TITLE,
        questions=[
            TextArea(
                title="",
                description=cases.EcjuQueries.AddQuery.DESCRIPTION,
                name="question",
                extras={"max_length": 5000,},
            ),
            HiddenField(name="form_name", value="ecju_query_write_or_edit_question"),
        ],
        back_link=BackLink("Back to " + cases.EcjuQueries.AddQuery.DROPDOWN_TITLE, choose_picklist_url),
        default_button_name="Continue",
    )


def create_ecju_create_confirmation_form():
    return confirm_form(
        title="Do you want to send your question?",
        confirmation_name="ecju_query_confirmation",
        back_link_text="Back to " + cases.EcjuQueries.AddQuery.TITLE,
        back_url="#",
        yes_label="Yes, send the question",
        no_label="No, edit the question",
        submit_button_text="Continue",
        hidden_field="ecju_query_create_confirmation",
    )
