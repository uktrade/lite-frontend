from django.urls import reverse
from django.conf import settings

from exporter.applications.forms.edit import firearms_form, reference_name_form, told_by_an_official_form
from exporter.apply_for_a_licence.forms.trade_control_licence import (
    application_type_form,
    activity_form,
    product_category_form,
)
from core.constants import GoodsTypeCategory
from exporter.core.constants import CaseTypes
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import (
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

from django.template.loader import render_to_string


def opening_question():
    options = [
        Option(
            key="export_licence",
            value="Export licence",
            description=(
                "Select if you’re sending products from the UK to another country. You need an export licence "
                "before you provide access to controlled technology, software or data."
            ),
        ),
        Option(
            key="transhipment",
            value="Transhipment licence",
            description=(
                "Select if you're shipping something from overseas through the UK on to another country. "
                "If the products will be in the UK for 30 days or more, apply for an export licence."
            ),
            disabled=settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
        ),
        Option(
            key="trade_control_licence",
            value="Trade control licence",
            description=(
                "Select if you’re arranging or brokering the sale or movement of controlled military products "
                "located overseas."
            ),
            disabled=settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
        ),
        Option(
            key="mod",
            value="MOD clearance",
            description=(
                "Select if you need to share information (an F680) or to go to an exhibition, or if you're gifting "
                "surplus products."
            ),
            disabled=settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
        ),
    ]
    if settings.FEATURE_FLAG_ONLY_ALLOW_SIEL:
        description = render_to_string("applications/use-spire-triage.html")
    else:
        description = ""

    return Form(
        title="Select what you need",
        description=description,
        questions=[RadioButtons(name="licence_type", options=options)],
        default_button_name="Continue",
        back_link=Breadcrumbs(
            [
                BackLink("Account home", reverse("core:home")),
                BackLink("Apply for a licence", ""),
            ]
        ),
    )


def export_permanency_form(application_type):
    return Form(
        title="Select an export type",
        description="",
        questions=[
            RadioButtons(
                name="export_type",
                options=[
                    Option("temporary", "Temporary"),
                    Option("permanent", "Permanent"),
                ],
            ),
        ],
        default_button_name="Continue" if application_type == CaseTypes.SIEL else "Save and continue",
    )


def export_type_form():
    options = [
        Option(
            key=CaseTypes.SIEL,
            value="Standard Individual Export Licence (SIEL)",
            description=(
                "Select to apply for a licence to export a set quantity and set value of products to 1 destination."
            ),
        ),
        Option(
            key=CaseTypes.OGEL,
            value="Open General Export Licence (OGEL)",
            description=(
                "Select to register a pre-published licence with set terms "
                "and conditions. Being an OGEL holder can benefit your business "
                "by saving time and money."
            ),
            disabled=settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
        ),
        Option(
            key=CaseTypes.OIEL,
            value="Open Individual Export Licence (OIEL)",
            description=(
                "Select to apply for a licence to export multiple shipments of specific products to specific "
                "destinations. OIELs cover long term projects and repeat business."
            ),
            disabled=settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
        ),
    ]
    help_url = "https://www.gov.uk/guidance/beginners-guide-to-export-controls#what-licence-do-i-need"
    if settings.FEATURE_FLAG_ONLY_ALLOW_SIEL:
        description = render_to_string("applications/use-spire-application-type.html")
    else:
        description = ""

    return Form(
        title="Select the type of export licence you need",
        description=description,
        questions=[
            RadioButtons(name="application_type", options=options),
            DetailComponent(
                "What licence do I need?", f"Read about the [different types of export control licences]({help_url})."
            ),
        ],
        default_button_name="Continue",
        back_link=BackLink("Back", reverse("apply_for_a_licence:start")),
    )


def export_licence_questions(request, application_type, goodstype_category=None):
    forms = [export_type_form()]

    if application_type == CaseTypes.OIEL:
        forms.append(goodstype_category_form())

    if application_type != CaseTypes.OGEL:
        forms.append(reference_name_form())

    if application_type == CaseTypes.SIEL:
        forms.append(told_by_an_official_form())

    if goodstype_category in [GoodsTypeCategory.MILITARY, GoodsTypeCategory.UK_CONTINENTAL_SHELF]:
        forms.append(firearms_form())

    return FormGroup(forms)


def goodstype_category_form(application_id=None):
    return Form(
        title=ExportLicenceQuestions.OpenLicenceCategoryQuestion.TITLE,
        questions=[
            RadioButtons(
                name="goodstype_category",
                options=[
                    Option(
                        key="military",
                        value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.MILITARY,
                    ),
                    Option(
                        key="cryptographic",
                        value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.CRYPTOGRAPHIC,
                    ),
                    Option(
                        key="media",
                        value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.MEDIA,
                    ),
                    Option(
                        key="uk_continental_shelf",
                        value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.UK_CONTINENTAL_SHELF,
                    ),
                    Option(
                        key="dealer",
                        value=ExportLicenceQuestions.OpenLicenceCategoryQuestion.DEALER,
                    ),
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
                    TranshipmentQuestions.TranshipmentLicenceQuestion.BACK, reverse("apply_for_a_licence:start")
                ),
            ),
            *conditional(
                request.POST.get("application_type") != CaseTypes.OGTL,
                [reference_name_form(), told_by_an_official_form()],
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
                back_link=BackLink(MODQuestions.WhatAreYouApplyingFor.BACK, reverse("apply_for_a_licence:start")),
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
