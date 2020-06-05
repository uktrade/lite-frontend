from django.urls import reverse_lazy

from applications.forms.edit import firearms_form, reference_name_form, told_by_an_official_form
from apply_for_a_licence.forms.trade_control_licence import application_type_form, activity_form, product_category_form
from conf.constants import CaseTypes, GoodsTypeCategory
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import (
    InitialApplicationQuestionsForms,
    ExportLicenceQuestions,
    MODQuestions,
    TranshipmentQuestions,
)
from lite_forms.components import (
    Form,
    RadioButtons,
    Option,
    Breadcrumbs,
    BackLink,
    FormGroup,
    DetailComponent,
    Label,
)
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
                        key="transhipment",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRANSHIPMENT_LICENCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRANSHIPMENT_LICENCE_DESCRIPTION,
                    ),
                    Option(
                        key="trade_control_licence",
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
                BackLink(generic.SERVICE_NAME, reverse_lazy("core:home")),
                BackLink(InitialApplicationQuestionsForms.OpeningQuestion.BREADCRUMB, ""),
            ]
        ),
    )


def export_licence_questions(request, application_type, goodstype_category=None):
    should_display_firearms_question = application_type == CaseTypes.SIEL or goodstype_category in [
        GoodsTypeCategory.MILITARY,
        GoodsTypeCategory.UK_CONTINENTAL_SHELF,
    ]

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
                                key=CaseTypes.OGEL,
                                value=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_GENERAL_EXPORT_LICENCE,
                                description=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_GENERAL_EXPORT_LICENCE_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.SIEL,
                                value=ExportLicenceQuestions.ExportLicenceQuestion.STANDARD_LICENCE,
                                description=ExportLicenceQuestions.ExportLicenceQuestion.STANDARD_LICENCE_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.OIEL,
                                value=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_LICENCE,
                                description=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_LICENCE_DESCRIPTION,
                            ),
                        ],
                    ),
                    DetailComponent(
                        InitialApplicationQuestionsForms.OpeningQuestion.HELP_WITH_CHOOSING_A_LICENCE,
                        InitialApplicationQuestionsForms.OpeningQuestion.HELP_WITH_CHOOSING_A_LICENCE_CONTENT,
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(
                    ExportLicenceQuestions.ExportLicenceQuestion.BACK, reverse_lazy("apply_for_a_licence:start")
                ),
            ),
            *conditional(application_type == CaseTypes.OIEL, [goodstype_category_form()], []),
            *conditional(
                application_type != CaseTypes.OGEL and goodstype_category not in ["media", "cryptographic"],
                [
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
                        default_button_name=generic.CONTINUE
                        if application_type == CaseTypes.SIEL
                        else generic.SAVE_AND_CONTINUE,
                    ),
                ],
                [],
            ),
            *conditional(application_type != CaseTypes.OGEL, [reference_name_form()], []),
            *conditional(application_type == CaseTypes.SIEL, [told_by_an_official_form()], []),
            *conditional(should_display_firearms_question, [firearms_form()], []),
        ]
    )


def goodstype_category_form(application_id=None):
    return Form(
        title=ExportLicenceQuestions.OpenLicenceCategoryQuestion.TITLE,
        questions=[
            RadioButtons(
                name="goodstype_category",
                options=[
                    Option(key="military", value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.MILITARY,),
                    Option(
                        key="cryptographic", value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.CRYPTOGRAPHIC,
                    ),
                    Option(key="media", value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.MEDIA,),
                    Option(
                        key="uk_continental_shelf",
                        value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.UK_CONTINENTAL_SHELF,
                    ),
                    Option(key="dealer", value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.DEALER,),
                ],
            )
        ],
        default_button_name=conditional(application_id, generic.SAVE_AND_RETURN, generic.CONTINUE),
    )


def trade_control_licence_questions(request):
    return FormGroup(
        [
            application_type_form(),
            *conditional(
                request.POST.get("application_type") != CaseTypes.OGTCL,
                [reference_name_form(), activity_form(request), product_category_form(request)],
                [],
            ),
        ]
    )


def transhipment_questions(request):
    return FormGroup(
        [
            Form(
                title=TranshipmentQuestions.TranshipmentLicenceQuestion.TITLE,
                description=TranshipmentQuestions.TranshipmentLicenceQuestion.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=CaseTypes.OGTL,
                                value=TranshipmentQuestions.TranshipmentLicenceQuestion.OPEN_GENERAL_TRANSHIPMENT_LICENCE,
                                description=TranshipmentQuestions.TranshipmentLicenceQuestion.OPEN_GENERAL_TRANSHIPMENT_LICENCE_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.SITL,
                                value=TranshipmentQuestions.TranshipmentLicenceQuestion.STANDARD_LICENCE,
                                description=TranshipmentQuestions.TranshipmentLicenceQuestion.STANDARD_LICENCE_DESCRIPTION,
                            ),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(
                    TranshipmentQuestions.TranshipmentLicenceQuestion.BACK, reverse_lazy("apply_for_a_licence:start")
                ),
            ),
            *conditional(
                request.POST.get("application_type") != CaseTypes.OGTL,
                [reference_name_form(), told_by_an_official_form(), firearms_form()],
                [],
            ),
        ]
    )


def MOD_questions(application_type=None):
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
                                key=CaseTypes.F680,
                                value=MODQuestions.WhatAreYouApplyingFor.PERMISSION_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.PERMISSION_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.EXHC,
                                value=MODQuestions.WhatAreYouApplyingFor.EXHIBITION_CLEARANCE_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.EXHIBITION_CLEARANCE_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.GIFT,
                                value=MODQuestions.WhatAreYouApplyingFor.GIFTING_CLEARANCE_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.GIFTING_CLEARANCE_DESCRIPTION,
                            ),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(MODQuestions.WhatAreYouApplyingFor.BACK, reverse_lazy("apply_for_a_licence:start")),
            ),
            conditional(
                application_type == CaseTypes.F680,
                Form(
                    title=MODQuestions.ConfirmationStatement.TITLE,
                    questions=[
                        Label(paragraph) for paragraph in MODQuestions.ConfirmationStatement.DESCRIPTION.split("\n")
                    ],
                    default_button_name=generic.CONFIRM_AND_CONTINUE,
                ),
            ),
            reference_name_form(),
        ]
    )
