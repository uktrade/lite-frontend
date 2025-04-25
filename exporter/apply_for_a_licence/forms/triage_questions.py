import rules

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.urls import reverse

from core.common.forms import (
    Choice,
    FieldsetForm,
)
from core.constants import GoodsTypeCategory
from core.forms.layouts import RenderTemplate
from exporter.applications.forms.edit import firearms_form, reference_name_form, told_by_an_official_form
from exporter.apply_for_a_licence.enums import LicenceType
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
    BackLink,
    FormGroup,
    Label,
)
from lite_forms.helpers import conditional


class LicenceTypeForm(FieldsetForm):
    class Layout:
        TITLE = "Select what you need"

    licence_type = forms.ChoiceField(
        choices=(
            Choice(
                LicenceType.EXPORT_LICENCE,
                "Export licence",
                hint="Select if you’re sending products from the UK to another country. You need an export licence "
                "before you provide access to controlled technology, software or data.",
            ),
            Choice(
                LicenceType.F680,
                "Form 680 (F680) security approval",
                hint="Select if you need approval to share classified items with non-UK entities. You should apply "
                "for security approval before you apply for  an export licence.",
            ),
            Choice(
                LicenceType.TRANSHIPMENT,
                "Transhipment licence",
                disabled=True,
                hint="Select if you're shipping something from overseas through the UK on to another country. If the "
                "products will be in the UK for 30 days or more, apply for an export licence.",
            ),
            Choice(
                LicenceType.TRADE_CONTROL_LICENCE,
                "Trade control licence",
                disabled=True,
                hint="Select if you’re arranging or brokering the sale or movement of controlled military products "
                "located overseas.",
            ),
        ),
        error_messages={
            "required": "Select the type of licence or approval you need",
        },
        label="",
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        licence_type_choices = {choice.value: choice for choice in self.fields["licence_type"].choices}
        f680_choice = licence_type_choices["f680"]
        f680_choice.disabled = not rules.test_rule("can_exporter_use_f680s", request)

    def get_layout_fields(self):
        return (
            RenderTemplate("applications/use-spire-triage.html"),
            "licence_type",
        )

    def clean_licence_type(self):
        valid_choices = [
            choice.value for choice in self.fields["licence_type"].choices if not getattr(choice, "disabled", False)
        ]
        value = self.cleaned_data["licence_type"]

        if value not in valid_choices:
            raise ValidationError(
                self.fields["licence_type"].error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )

        return value


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
    if settings.FEATURE_FLAG_ONLY_ALLOW_SIEL:
        description = render_to_string("applications/use-spire-application-type.html")
    else:
        description = ""

    return Form(
        title="Select the type of export licence you need",
        description=description,
        questions=[
            RadioButtons(name="application_type", options=options),
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


def transhipment_questions(request):
    return FormGroup(
        [
            Form(
                title=TranshipmentQuestions.TranshipmentLicenceQuestion.TITLE,
                description="",
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=CaseTypes.OGTL,
                                value=TranshipmentQuestions.TranshipmentLicenceQuestion.OPEN_GENERAL_TRANSHIPMENT_LICENCE,
                                description=(
                                    "Select to register a pre-published licence with set terms and conditions. Being an OGTL holder can benefit your "
                                    "business by saving time and money."
                                ),
                            ),
                            Option(
                                key=CaseTypes.SITL,
                                value=TranshipmentQuestions.TranshipmentLicenceQuestion.STANDARD_LICENCE,
                                description="Select a standard transhipment licence for a set quantity and set value of products",
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
                description="",
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
