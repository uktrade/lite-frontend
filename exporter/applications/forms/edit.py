from exporter.applications.components import back_to_task_list
from lite_content.lite_exporter_frontend import applications, generic, strings
from lite_content.lite_exporter_frontend.applications import ExportLicenceQuestions
from lite_forms.components import Form, TextInput, Option, RadioButtons
from lite_forms.helpers import conditional


def reference_name_form(application_id=None):
    return Form(
        title=applications.InitialApplicationQuestionsForms.ReferenceNameQuestion.TITLE,
        description=applications.InitialApplicationQuestionsForms.ReferenceNameQuestion.DESCRIPTION,
        questions=[
            TextInput(name="name"),
        ],
        back_link=back_to_task_list(application_id),
        default_button_name=conditional(application_id, generic.SAVE_AND_RETURN, generic.CONTINUE),
    )


def firearms_form(application_id=None):
    return Form(
        title=applications.GoodsCategories.TITLE,
        description=applications.GoodsCategories.DESCRIPTION,
        questions=[
            RadioButtons(
                name="contains_firearm_goods",
                options=[
                    Option(key="True", value=strings.YES),
                    Option(key="False", value=strings.NO),
                ],
            ),
        ],
        back_link=back_to_task_list(application_id),
        default_button_name=conditional(application_id, generic.SAVE_AND_RETURN, generic.CONTINUE),
    )


def told_by_an_official_form(application_id=None):
    return Form(
        title=ExportLicenceQuestions.HaveYouBeenInformedQuestion.TITLE,
        description=ExportLicenceQuestions.HaveYouBeenInformedQuestion.DESCRIPTION,
        questions=[
            RadioButtons(
                name="have_you_been_informed",
                options=[
                    Option(
                        key="yes",
                        value=strings.YES,
                        components=[
                            TextInput(
                                title=ExportLicenceQuestions.HaveYouBeenInformedQuestion.WHAT_WAS_THE_REFERENCE_CODE_TITLE,
                                description=ExportLicenceQuestions.HaveYouBeenInformedQuestion.WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION,
                                name="reference_number_on_information_form",
                                optional=True,
                            ),
                        ],
                    ),
                    Option(key="no", value=strings.NO),
                ],
            ),
        ],
        back_link=back_to_task_list(application_id),
        default_button_name=conditional(application_id, generic.SAVE_AND_RETURN, generic.CONTINUE),
    )
