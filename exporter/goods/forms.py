from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe

from exporter.core.constants import PRODUCT_CATEGORY_FIREARM
from core.builtins.custom_tags import linkify
from exporter.core.services import get_control_list_entries
from exporter.core.services import get_pv_gradings
from exporter.goods.helpers import good_summary, get_category_display_string, get_sporting_shotgun_form_title
from exporter.goods.services import get_document_missing_reasons
from lite_content.lite_exporter_frontend.generic import PERMISSION_FINDER_LINK
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.goods import (
    CreateGoodForm,
    GoodsQueryForm,
    EditGoodForm,
    DocumentSensitivityForm,
    AttachDocumentForm,
    GoodsList,
    GoodGradingForm,
)
from lite_forms.common import control_list_entries_question
from lite_forms.components import (
    Form,
    HTMLBlock,
    TextArea,
    RadioButtons,
    Option,
    BackLink,
    Custom,
    FileUpload,
    TextInput,
    HiddenField,
    Button,
    DateInput,
    Label,
    Select,
    Group,
    Breadcrumbs,
    FormGroup,
    Heading,
    HelpSection,
    Checkboxes,
)
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle, HeadingStyle


def product_category_form(request):
    return Form(
        title=CreateGoodForm.ProductCategory.TITLE,
        questions=[
            RadioButtons(
                title="",
                name="item_category",
                options=[
                    Option(key="group1_platform", value=CreateGoodForm.ProductCategory.GROUP1_PLATFORM),
                    Option(key="group1_device", value=CreateGoodForm.ProductCategory.GROUP1_DEVICE),
                    Option(key="group1_components", value=CreateGoodForm.ProductCategory.GROUP1_COMPONENTS),
                    Option(key="group1_materials", value=CreateGoodForm.ProductCategory.GROUP1_MATERIALS),
                    Option(key=PRODUCT_CATEGORY_FIREARM, value=CreateGoodForm.ProductCategory.GROUP2_FIREARMS),
                    Option(key="group3_software", value=CreateGoodForm.ProductCategory.GROUP3_SOFTWARE),
                    Option(key="group3_technology", value=CreateGoodForm.ProductCategory.GROUP3_TECHNOLOGY),
                ],
            )
        ],
    )


def software_technology_details_form(request, category_type):
    category_text = get_category_display_string(category_type)

    return Form(
        title=CreateGoodForm.TechnologySoftware.TITLE + category_text,
        questions=[
            HiddenField("is_software_or_technology_step", True),
            TextArea(title="", description="", name="software_or_technology_details", optional=False,),
        ],
    )


def product_military_use_form(request):
    return Form(
        title=CreateGoodForm.MilitaryUse.TITLE,
        questions=[
            HiddenField("is_military_use_step", True),
            RadioButtons(
                title="",
                name="is_military_use",
                options=[
                    Option(key="yes_designed", value=CreateGoodForm.MilitaryUse.YES_DESIGNED),
                    Option(
                        key="yes_modified",
                        value=CreateGoodForm.MilitaryUse.YES_MODIFIED,
                        components=[
                            TextArea(
                                title=CreateGoodForm.MilitaryUse.MODIFIED_MILITARY_USE_DETAILS,
                                description="",
                                name="modified_military_use_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key="no", value=CreateGoodForm.MilitaryUse.NO),
                ],
            ),
        ],
    )


def product_component_form(request):
    return Form(
        title=CreateGoodForm.ProductComponent.TITLE,
        questions=[
            HiddenField("is_component_step", True),
            RadioButtons(
                title="",
                name="is_component",
                options=[
                    Option(
                        key="yes_designed",
                        value=CreateGoodForm.ProductComponent.YES_DESIGNED,
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductComponent.DESIGNED_DETAILS,
                                description="",
                                name="designed_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(
                        key="yes_modified",
                        value=CreateGoodForm.ProductComponent.YES_MODIFIED,
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductComponent.MODIFIED_DETAILS,
                                description="",
                                name="modified_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(
                        key="yes_general",
                        value=CreateGoodForm.ProductComponent.YES_GENERAL_PURPOSE,
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductComponent.GENERAL_DETAILS,
                                description="",
                                name="general_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key="no", value=CreateGoodForm.ProductComponent.NO),
                ],
            ),
        ],
    )


def product_uses_information_security(request):
    return Form(
        title=CreateGoodForm.ProductInformationSecurity.TITLE,
        questions=[
            HiddenField("is_information_security_step", True),
            RadioButtons(
                title="",
                name="uses_information_security",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductInformationSecurity.INFORMATION_SECURITY_DETAILS,
                                description="",
                                name="information_security_details",
                                optional=True,
                            ),
                        ],
                    ),
                    Option(key=False, value=CreateGoodForm.ProductInformationSecurity.NO),
                ],
            ),
        ],
    )


def add_goods_questions(control_list_entries, application_pk=None):

    is_good_controlled_description = (
        f"Products that aren't on the {PERMISSION_FINDER_LINK} may be affected by [military end use controls]"
        "(https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
        "[current trade sanctions and embargoes]"
        "(https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
        "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
        "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
    )

    is_pv_graded_description = (
        "For example, UK OFFICIAL or NATO UNCLASSIFIED. The security grading of the product doesn't affect "
        "if an export licence is needed."
    )

    is_good_controlled_options = [
        Option(
            key=True,
            value="Yes",
            components=[
                control_list_entries_question(
                    control_list_entries=control_list_entries,
                    title="Control list entries",
                    description="Type to get suggestions. For example, ML1a.",
                ),
            ],
        ),
        Option(key=False, value="No"),
    ]

    is_pv_graded_options = [
        Option(key="yes", value="Yes"),
        Option(key="no", value="No, it doesn't need one"),
    ]

    if settings.FEATURE_FLAG_ONLY_ALLOW_SIEL:
        if not application_pk:
            controlled_spire = HelpSection(
                description=mark_safe(  # nosec
                    f"Use <a href='{settings.SPIRE_URL}'>SPIRE</a> to raise a control list classification (CLC) query"
                ),
                title="",
            )
            pv_graded_spire = HelpSection(
                description=mark_safe(  # nosec
                    f"Use <a href='{settings.SPIRE_URL}'>SPIRE</a> to apply for a private venture (PV) grading",
                ),
                title="",
            )
            is_good_controlled_options.append(Option(key=None, value="I don't know", components=[controlled_spire]))
            is_pv_graded_options.append(
                Option(key="grading_required", value="No, it needs one", components=[pv_graded_spire])
            )
    else:
        if not application_pk:
            is_good_controlled_options.append(
                Option(key=None, value="I don't know, raise a control list classification (CLC) query")
            )
            is_pv_graded_options.append(
                Option(key="grading_required", value="No, it needs one, apply for a private venture (PV) grading")
            )
    return Form(
        title=conditional(application_pk, "Add a product to your application", "Add a product to your product list"),
        questions=[
            TextInput(
                title="Name",
                description=("Give your product a name so it is easier to find in your product list"),
                name="name",
            ),
            TextArea(title="Description", name="description", extras={"max_length": 280}, rows=5, optional=True,),
            TextInput(title="Part number", name="part_number", optional=True),
            RadioButtons(
                title="Is the product on the control list?",
                description=is_good_controlled_description,
                name="is_good_controlled",
                options=is_good_controlled_options,
            ),
            RadioButtons(
                title="Does the product have a security grading?",
                description=is_pv_graded_description,
                name="is_pv_graded",
                options=is_pv_graded_options,
            ),
        ],
        back_link=conditional(
            application_pk,
            BackLink("Back", reverse_lazy("applications:goods", kwargs={"pk": application_pk})),
            Breadcrumbs(
                [
                    BackLink(generic.SERVICE_NAME, reverse_lazy("core:home")),
                    BackLink(GoodsList.TITLE, reverse_lazy("goods:goods")),
                    BackLink(GoodsList.CREATE_GOOD),
                ]
            ),
        ),
        default_button_name="Continue",
    )


def edit_grading_form(request, good_id):
    return Form(
        title=CreateGoodForm.IsGraded.TITLE,
        description="",
        questions=[
            RadioButtons(
                name="is_pv_graded",
                options=[
                    Option(key="yes", value=CreateGoodForm.IsGraded.YES, components=pv_details_form(request).questions),
                    Option(key="no", value=CreateGoodForm.IsGraded.NO),
                ],
            )
        ],
        back_link=BackLink(CreateGoodForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
    )


def pv_details_form(request):
    return Form(
        title=GoodGradingForm.TITLE,
        description=GoodGradingForm.DESCRIPTION,
        questions=[
            Heading("PV grading", HeadingStyle.M),
            Group(
                components=[
                    TextInput(title=GoodGradingForm.PREFIX, name="prefix", optional=True),
                    Select(
                        options=get_pv_gradings(request, convert_to_options=True),
                        title=GoodGradingForm.GRADING,
                        name="grading",
                        optional=True,
                    ),
                    TextInput(title=GoodGradingForm.SUFFIX, name="suffix", optional=True),
                ],
                classes=["app-pv-grading-inputs"],
            ),
            TextInput(title=GoodGradingForm.OTHER_GRADING, name="custom_grading", optional=True),
            TextInput(title=GoodGradingForm.ISSUING_AUTHORITY, name="issuing_authority"),
            TextInput(title=GoodGradingForm.REFERENCE, name="reference"),
            DateInput(
                title=GoodGradingForm.DATE_OF_ISSUE, prefix="date_of_issue", name="date_of_issue", optional=False
            ),
        ],
        default_button_name=GoodGradingForm.BUTTON,
    )


def add_good_form_group(
    request,
    is_pv_graded: bool = None,
    is_software_technology: bool = None,
    is_firearm: bool = None,
    is_firearms_core: bool = None,
    is_firearms_accessory: bool = None,
    is_firearms_software_tech: bool = None,
    draft_pk: str = None,
    base_form_back_link: str = None,
):
    control_list_entries = get_control_list_entries(request, convert_to_options=True)
    return FormGroup(
        [
            group_two_product_type_form(back_link=base_form_back_link),
            conditional(is_firearms_core and draft_pk, identification_markings_form()),
            conditional(is_firearms_core, firearms_sporting_shotgun_form(request.POST.get("type"))),
            add_goods_questions(control_list_entries, draft_pk),
            conditional(is_pv_graded, pv_details_form(request)),
            # only ask if adding to a draft application
            conditional(is_firearm and bool(draft_pk), firearm_year_of_manufacture_details_form()),
            conditional(is_firearm, firearm_replica_form(request.POST.get("type"))),
            conditional(is_firearms_core, firearm_calibre_details_form()),
            conditional(is_firearms_core and bool(draft_pk), firearms_act_confirmation_form()),
            conditional(is_firearms_software_tech, software_technology_details_form(request, request.POST.get("type"))),
            conditional(is_firearms_accessory or is_firearms_software_tech, product_military_use_form(request)),
            conditional(is_firearms_accessory, product_component_form(request)),
            conditional(is_firearms_accessory or is_firearms_software_tech, product_uses_information_security(request)),
        ]
    )


def add_firearm_good_form_group(request, is_pv_graded: bool = None, draft_pk: str = None):
    control_list_entries = get_control_list_entries(request, convert_to_options=True)
    return FormGroup(
        [
            add_goods_questions(control_list_entries, draft_pk),
            conditional(is_pv_graded, pv_details_form(request)),
            group_two_product_type_form(),
            firearm_year_of_manufacture_details_form(),
            firearm_calibre_details_form(),
            firearms_act_confirmation_form(),
            identification_markings_form(),
        ]
    )


def edit_good_detail_form(request, good_id):
    return Form(
        title=EditGoodForm.TITLE,
        description=EditGoodForm.DESCRIPTION,
        questions=[
            TextInput(
                title="Name",
                description=("Give your product a name so it is easier to find in your product list"),
                name="name",
            ),
            TextArea(
                title=EditGoodForm.Description.TITLE,
                name="description",
                rows=5,
                optional=True,
                extras={"max_length": 280},
            ),
            TextInput(title=EditGoodForm.PartNumber.TITLE, name="part_number", optional=True),
            RadioButtons(
                title=EditGoodForm.IsControlled.TITLE,
                description=EditGoodForm.IsControlled.DESCRIPTION,
                name="is_good_controlled",
                options=[
                    Option(
                        key=True,
                        value=EditGoodForm.IsControlled.YES,
                        components=[
                            control_list_entries_question(
                                control_list_entries=get_control_list_entries(request, convert_to_options=True),
                                title=EditGoodForm.ControlListEntry.TITLE,
                                description=EditGoodForm.ControlListEntry.DESCRIPTION,
                            ),
                        ],
                    ),
                    Option(key=False, value=EditGoodForm.IsControlled.NO),
                ],
            ),
        ],
        back_link=BackLink(CreateGoodForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
    )


def document_grading_form(request, good_id, back_url=None):
    select_options = get_document_missing_reasons(request)[0]["reasons"]

    if back_url:
        link = back_url
    else:
        link = reverse_lazy("goods:good", kwargs={"pk": good_id})

    return Form(
        title=DocumentSensitivityForm.TITLE,
        description=DocumentSensitivityForm.DESCRIPTION,
        questions=[
            RadioButtons(
                name="has_document_to_upload",
                options=[
                    Option(key="yes", value=DocumentSensitivityForm.Options.YES),
                    Option(
                        key="no",
                        value=DocumentSensitivityForm.Options.NO,
                        components=[
                            Label(text=DocumentSensitivityForm.ECJU_HELPLINE),
                            Select(
                                name="missing_document_reason",
                                title=DocumentSensitivityForm.LABEL,
                                options=select_options,
                            ),
                        ],
                    ),
                ],
            ),
        ],
        back_link=BackLink(DocumentSensitivityForm.BACK_BUTTON, link),
        default_button_name=DocumentSensitivityForm.SUBMIT_BUTTON,
    )


def attach_documents_form(back_link):
    return Form(
        title=AttachDocumentForm.TITLE,
        description=AttachDocumentForm.DESCRIPTION,
        questions=[
            FileUpload(),
            TextArea(
                title=AttachDocumentForm.Description.TITLE,
                optional=True,
                name="description",
                extras={"max_length": 280},
            ),
        ],
        buttons=[Button(AttachDocumentForm.BUTTON, "submit")],
        back_link=back_link,
    )


def raise_a_goods_query(good_id, raise_a_clc: bool, raise_a_pv: bool):
    questions = []

    if raise_a_clc:
        if GoodsQueryForm.CLCQuery.TITLE:
            questions += [
                Heading(GoodsQueryForm.CLCQuery.TITLE, HeadingStyle.M),
            ]
        questions += [
            TextInput(
                title=GoodsQueryForm.CLCQuery.Code.TITLE,
                description=GoodsQueryForm.CLCQuery.Code.DESCRIPTION,
                name="clc_control_code",
                optional=True,
            ),
            TextArea(title=GoodsQueryForm.CLCQuery.Details.TITLE, name="clc_raised_reasons", optional=True,),
        ]

    if raise_a_pv:
        if GoodsQueryForm.PVGrading.TITLE:
            questions += [
                Heading(GoodsQueryForm.PVGrading.TITLE, HeadingStyle.M),
            ]
        questions += [
            TextArea(title=GoodsQueryForm.PVGrading.Details.TITLE, name="pv_grading_raised_reasons", optional=True,),
        ]

    return Form(
        title=GoodsQueryForm.TITLE,
        description=GoodsQueryForm.DESCRIPTION,
        questions=questions,
        back_link=BackLink(GoodsQueryForm.BACK_LINK, reverse("goods:good", kwargs={"pk": good_id})),
        default_button_name="Save",
    )


def delete_good_form(good):
    return Form(
        title=EditGoodForm.DeleteConfirmationForm.TITLE,
        questions=[good_summary(good)],
        buttons=[
            Button(value=EditGoodForm.DeleteConfirmationForm.YES, action="submit", style=ButtonStyle.WARNING),
            Button(
                value=EditGoodForm.DeleteConfirmationForm.NO,
                action="",
                style=ButtonStyle.SECONDARY,
                link=reverse_lazy("goods:good", kwargs={"pk": good["id"]}),
            ),
        ],
    )


def group_two_product_type_form(back_link=None):
    form = Form(
        title=CreateGoodForm.FirearmGood.ProductType.TITLE,
        questions=[
            HiddenField("product_type_step", True),
            RadioButtons(
                title="",
                name="type",
                options=[
                    Option(key="firearms", value=CreateGoodForm.FirearmGood.ProductType.FIREARM),
                    Option(key="ammunition", value=CreateGoodForm.FirearmGood.ProductType.AMMUNITION),
                    Option(
                        key="components_for_firearms",
                        value=CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_FIREARM,
                    ),
                    Option(
                        key="components_for_ammunition",
                        value=CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_AMMUNITION,
                    ),
                    Option(key="firearms_accessory", value=CreateGoodForm.FirearmGood.ProductType.FIREARMS_ACCESSORY),
                    Option(
                        key="software_related_to_firearms",
                        value=CreateGoodForm.FirearmGood.ProductType.SOFTWARE_RELATED_TO_FIREARM,
                    ),
                    Option(
                        key="technology_related_to_firearms",
                        value=CreateGoodForm.FirearmGood.ProductType.TECHNOLOGY_RELATED_TO_FIREARM,
                    ),
                ],
            ),
        ],
        default_button_name="Save and continue",
    )

    if back_link:
        form.back_link = BackLink("Back", back_link)

    return form


def firearms_sporting_shotgun_form(firearm_type):
    title = get_sporting_shotgun_form_title(firearm_type)

    return Form(
        title=title,
        questions=[
            HiddenField("type", firearm_type),
            HiddenField("sporting_shotgun_step", True),
            RadioButtons(
                title="",
                name="is_sporting_shotgun",
                options=[Option(key=True, value="Yes"), Option(key=False, value="No"),],
            ),
        ],
        default_button_name="Save and continue",
    )


def firearm_year_of_manufacture_details_form(good_id=None):
    return Form(
        title="What is the year of manufacture of the firearm?",
        default_button_name="Save and continue",
        questions=list(
            filter(
                bool,
                [
                    HiddenField("good_id", good_id) if good_id else None,
                    HiddenField("firearm_year_of_manufacture_step", True),
                    TextInput(description="", name="year_of_manufacture", optional=False,),
                ],
            )
        ),
    )


def firearm_replica_form(firearm_type):
    return Form(
        title=CreateGoodForm.FirearmGood.FirearmsReplica.TITLE,
        default_button_name="Save and continue",
        questions=[
            HiddenField("type", firearm_type),
            HiddenField("is_replica_step", True),
            RadioButtons(
                title="",
                name="is_replica",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=CreateGoodForm.FirearmGood.FirearmsReplica.DESCRIPTION,
                                description="",
                                name="replica_description",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No",),
                ],
            ),
        ],
    )


def firearm_calibre_details_form():
    return Form(
        title="What is the calibre of the product?",
        default_button_name="Save and continue",
        questions=[
            HiddenField("firearm_calibre_step", True),
            TextInput(title="", description="", name="calibre", optional=False,),
        ],
    )


def format_list_item(link, name, description):
    return "<br>" + "<li>" + linkify(link, name=name,) + f"&nbsp;&nbsp;{description}" + "</li>"


def firearms_act_confirmation_form():
    return Form(
        title=CreateGoodForm.FirearmGood.FirearmsActCertificate.TITLE,
        default_button_name="Save and continue",
        questions=[
            HiddenField("section_certificate_step", True),
            HTMLBlock(
                "<br>"
                + "<details class='govuk-details' data-module='govuk-details'>"
                + "<summary class='govuk-details__summary'>"
                + "    <span class='govuk-details__summary-text'>What do the sections cover?</span>"
                + "</summary>"
                + "<div>"
                + " <ol class='govuk-list govuk-!-padding-left-8'>"
                + format_list_item(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE_LINK,
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE,
                    "  is a broad category covering most types of firearm and ammunition, including rifles and high powered air weapons.",
                )
                + format_list_item(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO_LINK,
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO,
                    "  covers most types of shotgun.",
                )
                + format_list_item(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE_LINK,
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE,
                    "  covers weapons and ammunition that are generally prohibited.",
                )
                + "</ol>"
                + "</div>"
                + "</details>"
                "<br>"
            ),
            RadioButtons(
                title="",
                name="is_covered_by_firearm_act_section_one_two_or_five",
                options=[
                    Option(
                        key="Yes",
                        value=CreateGoodForm.FirearmGood.FirearmsActCertificate.YES,
                        components=[
                            RadioButtons(
                                title="Select section",
                                name="firearms_act_section",
                                options=[
                                    Option(key="firearms_act_section1", value="Section 1"),
                                    Option(key="firearms_act_section2", value="Section 2"),
                                ],
                            )
                        ],
                    ),
                    Option(key="No", value=CreateGoodForm.FirearmGood.FirearmsActCertificate.NO),
                    Option(key="Unsure", value=CreateGoodForm.FirearmGood.FirearmsActCertificate.DONT_KNOW),
                ],
            ),
        ],
        javascript_imports={"/javascripts/add-good.js"},
    )


def upload_firearms_act_certificate_form(section, filename, back_link):
    return Form(
        title=f"Upload your Firearms Act 1968 {section} certificate",
        description="The file must be smaller than 50MB",
        questions=[
            HiddenField("firearms_certificate_uploaded", False),
            FileUpload(),
            HiddenField("uploaded_file_name", filename),
            TextInput(
                title=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_CERTIFICATE_NUMBER,
                description="",
                name="section_certificate_number",
                optional=False,
            ),
            DateInput(
                title=CreateGoodForm.FirearmGood.FirearmsActCertificate.EXPIRY_DATE,
                description=CreateGoodForm.FirearmGood.FirearmsActCertificate.EXPIRY_DATE_HINT,
                prefix="section_certificate_date_of_expiry",
                name="section_certificate_date_of_expiry",
            ),
            Label(text="Or"),
            Checkboxes(
                name="section_certificate_missing",
                options=[Option(key="True", value=f"I do not have a Firearms Act 1968 {section} certificate",)],
            ),
            TextArea(
                title="Provide a reason why you do not have a certificate",
                name="section_certificate_missing_reason",
                optional=False,
            ),
        ],
        back_link=back_link,
        buttons=[Button("Save and continue", "submit")],
        javascript_imports={"/javascripts/add-good.js"},
    )


def build_firearm_back_link_create(form_url, form_data):
    return Custom(
        data={**form_data, "form_pk": int(form_data["form_pk"]) + 1, "form_url": form_url,},
        template="applications/firearm_upload_back_link.html",
    )


def build_firearm_create_back(back_link):
    return BackLink("Back", back_link)


def identification_markings_form(draft_pk=None, good_id=None):
    questions = [
        HiddenField("identification_markings_step", True),
        RadioButtons(
            title="",
            name="has_identification_markings",
            options=[
                Option(
                    key=True,
                    value=CreateGoodForm.FirearmGood.IdentificationMarkings.YES,
                    components=[
                        TextArea(
                            title=CreateGoodForm.FirearmGood.IdentificationMarkings.MARKINGS_DETAILS,
                            description=CreateGoodForm.FirearmGood.IdentificationMarkings.MARKINGS_HELP_TEXT,
                            name="identification_markings_details",
                            optional=False,
                        ),
                    ],
                ),
                Option(
                    key=False,
                    value=CreateGoodForm.FirearmGood.IdentificationMarkings.NO,
                    components=[
                        TextArea(
                            title=CreateGoodForm.FirearmGood.IdentificationMarkings.NO_MARKINGS_DETAILS,
                            description="",
                            name="no_identification_markings_details",
                            optional=False,
                        )
                    ],
                ),
            ],
        ),
        HiddenField("pk", draft_pk) if draft_pk else None,
        HiddenField("good_id", good_id) if good_id else None,
    ]

    return Form(
        title=CreateGoodForm.FirearmGood.IdentificationMarkings.TITLE,
        questions=questions,
        default_button_name="Save and continue",
    )
