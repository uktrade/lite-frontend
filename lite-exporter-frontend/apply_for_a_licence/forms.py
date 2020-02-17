from django.urls import reverse_lazy

from conf.constants import STANDARD, OPEN, EXHIBITION, F680, GIFTING
from applications.forms.edit import goods_categories, reference_name_form
from lite_content.lite_exporter_frontend import strings, generic
from lite_content.lite_exporter_frontend.applications import (
    InitialApplicationQuestionsForms,
    ExportLicenceQuestions,
    MODQuestions,
)
from lite_forms.components import RadioButtons, Form, TextInput, Option, FormGroup, Breadcrumbs, BackLink
from lite_forms.helpers import conditional


def opening_question():
    return Form(
        title=InitialApplicationQuestionsForms.OpeningQuestion.TITLE,
        description=InitialApplicationQuestionsForms.OpeningQuestion.DESCRIPTION,
        questions=[
            RadioButtons(
                name="licence_type",
                options=[
                    Option(
                        key="export_licence",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.EXPORT_LICENCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.EXPORT_LICENCE_DESCRIPTION,
                    ),
                    Option(
                        key="export_licence",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRANSHIPMENT_LICENCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRANSHIPMENT_LICENCE_DESCRIPTION,
                    ),
                    Option(
                        key="export_licence",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRADE_CONTROL_LICENCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRADE_CONTROL_LICENCE_DESCRIPTION,
                    ),
                    Option(
                        key="mod",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.MOD_CLEARANCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.MOD_CLEARANCE_DESCRIPTION,
                    ),
                ],
            ),
        ],
        default_button_name=generic.CONTINUE,
        back_link=Breadcrumbs(
            [
                BackLink(generic.SERVICE_NAME, reverse_lazy("core:hub")),
                BackLink(InitialApplicationQuestionsForms.OpeningQuestion.BREADCRUMB, ""),
            ]
        ),
    )


def export_licence_questions(application_type):
    return FormGroup(
        [
            Form(
                title=ExportLicenceQuestions.ExportLicenceQuestion.TITLE,
                description=ExportLicenceQuestions.ExportLicenceQuestion.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=STANDARD,
                                value=ExportLicenceQuestions.ExportLicenceQuestion.STANDARD_LICENCE,
                                description=ExportLicenceQuestions.ExportLicenceQuestion.STANDARD_LICENCE_DESCRIPTION,
                            ),
                            Option(
                                key=OPEN,
                                value=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_LICENCE,
                                description=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_LICENCE_DESCRIPTION,
                            ),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(
                    ExportLicenceQuestions.ExportLicenceQuestion.BACK, reverse_lazy("apply_for_a_licence:start")
                ),
            ),
            reference_name_form(),
            Form(
                title=ExportLicenceQuestions.ExportType.TITLE,
                description=ExportLicenceQuestions.ExportType.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="export_type",
                        options=[
                            Option("temporary", ExportLicenceQuestions.ExportType.TEMPORARY),
                            Option("permanent", ExportLicenceQuestions.ExportType.PERMANENT),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE if application_type == STANDARD else generic.SAVE_AND_CONTINUE,
            ),
            *conditional(
                application_type != OPEN,
                [
                    goods_categories(),
                    Form(
                        title=ExportLicenceQuestions.HaveYouBeenInformedQuestion.TITLE,
                        description=ExportLicenceQuestions.HaveYouBeenInformedQuestion.DESCRIPTION,
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
                                title=ExportLicenceQuestions.HaveYouBeenInformedQuestion.WHAT_WAS_THE_REFERENCE_CODE_TITLE,
                                description=ExportLicenceQuestions.HaveYouBeenInformedQuestion.WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION,
                                name="reference_number_on_information_form",
                                optional=True,
                            ),
                        ],
                        default_button_name=generic.SAVE_AND_CONTINUE,
                    ),
                ],
                [],
            ),
        ]
    )


def MOD_questions():
    return FormGroup(
        [
            Form(
                title=MODQuestions.WhatAreYouApplyingFor.TITLE,
                description=MODQuestions.WhatAreYouApplyingFor.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=F680,
                                value=MODQuestions.WhatAreYouApplyingFor.PERMISSION_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.PERMISSION_DESCRIPTION,
                            ),
                            Option(
                                key=EXHIBITION,
                                value=MODQuestions.WhatAreYouApplyingFor.EXHIBITION_CLEARANCE_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.EXHIBITION_CLEARANCE_DESCRIPTION,
                            ),
                            Option(
                                key=GIFTING,
                                value=MODQuestions.WhatAreYouApplyingFor.GIFTING_CLEARANCE_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.GIFTING_CLEARANCE_DESCRIPTION,
                            ),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(MODQuestions.WhatAreYouApplyingFor.BACK, reverse_lazy("apply_for_a_licence:start")),
            ),
            reference_name_form(),
        ]
    )
