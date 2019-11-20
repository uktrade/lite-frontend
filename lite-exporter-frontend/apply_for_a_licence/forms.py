from conf.constants import STANDARD_LICENCE, OPEN_LICENCE
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import RadioButtons, Form, DetailComponent, TextInput, Option, FormGroup
from lite_forms.helpers import conditional


def initial_questions(application_type):
    return FormGroup(
        [
            Form(
                title=strings.WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE,
                description=strings.WHICH_EXPORT_LICENCE_DO_YOU_WANT_DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=STANDARD_LICENCE,
                                value=strings.STANDARD_LICENCE,
                                description=strings.STANDARD_LICENCE_DESCRIPTION,
                            ),
                            Option(
                                key=OPEN_LICENCE,
                                value=strings.OPEN_LICENCE,
                                description=strings.OPEN_LICENCE_DESCRIPTION,
                            ),
                        ],
                    ),
                    DetailComponent(strings.HELP_WITH_CHOOSING_A_LICENCE, strings.HELP_WITH_CHOOSING_A_LICENCE_CONTENT),
                ],
                default_button_name=strings.CONTINUE,
            ),
            Form(
                title=strings.ENTER_A_REFERENCE_NAME_TITLE,
                description=strings.ENTER_A_REFERENCE_NAME_DESCRIPTION,
                questions=[TextInput(name="name"),],
                default_button_name=strings.CONTINUE,
            ),
            Form(
                title=strings.TEMPORARY_OR_PERMANENT_TITLE,
                description=strings.TEMPORARY_OR_PERMANENT_DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="export_type",
                        options=[Option("temporary", strings.TEMPORARY), Option("permanent", strings.PERMANENT)],
                    ),
                ],
                default_button_name=strings.CONTINUE
                if application_type == STANDARD_LICENCE
                else strings.SAVE_AND_CONTINUE,
            ),
            conditional(
                application_type != OPEN_LICENCE,
                Form(
                    title=strings.HAVE_YOU_BEEN_INFORMED_TITLE,
                    description=strings.HAVE_YOU_BEEN_INFORMED_DESCRIPTION,
                    questions=[
                        RadioButtons(
                            name="have_you_been_informed",
                            options=[
                                Option("yes", strings.YES, show_pane="pane_reference_number_on_information_form"),
                                Option("no", strings.NO),
                            ],
                            classes=["govuk-radios--inline"],
                        ),
                        TextInput(
                            title=strings.WHAT_WAS_THE_REFERENCE_CODE_TITLE,
                            description=strings.WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION,
                            name="reference_number_on_information_form",
                            optional=True,
                        ),
                    ],
                    default_button_name=strings.SAVE_AND_CONTINUE,
                ),
            ),
        ]
    )
