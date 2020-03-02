from django.urls import reverse, reverse_lazy

from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.goods import (
    CreateGoodForm,
    GoodsQueryForm,
    EditGoodForm,
    DocumentSensitivityForm,
    AttachDocumentForm,
    RespondToQueryForm,
    GoodsList,
    GoodGradingForm,
)

from core.services import get_control_list_entries
from core.services import get_pv_gradings
from goods.helpers import good_summary
from goods.services import get_document_missing_reasons
from lite_forms.common import control_list_entry_question
from lite_forms.components import (
    Form,
    TextArea,
    RadioButtons,
    Option,
    BackLink,
    FileUpload,
    TextInput,
    HTMLBlock,
    HiddenField,
    Button,
    DateInput,
    Label,
    Select,
    Group,
    Breadcrumbs,
    FormGroup,
    Heading,
)
from lite_forms.generators import confirm_form
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle, HeadingStyle


def add_goods_questions(application_pk=None):
    return Form(
        title=conditional(application_pk, CreateGoodForm.TITLE_APPLICATION, CreateGoodForm.TITLE_GOODS_LIST),
        questions=[
            TextArea(
                title=CreateGoodForm.Description.TITLE,
                description=CreateGoodForm.Description.DESCRIPTION,
                name="description",
                extras={"max_length": 280},
            ),
            TextInput(title=CreateGoodForm.PartNumber.TITLE, name="part_number", optional=True),
            RadioButtons(
                title=CreateGoodForm.IsControlled.TITLE,
                description=conditional(
                    application_pk, CreateGoodForm.IsControlled.DESCRIPTION, CreateGoodForm.IsControlled.CLC_REQUIRED,
                ),
                name="is_good_controlled",
                options=[
                    Option(
                        key="yes",
                        value=CreateGoodForm.IsControlled.YES,
                        components=[
                            control_list_entry_question(
                                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                                title=CreateGoodForm.ControlListEntry.TITLE,
                                description=CreateGoodForm.ControlListEntry.DESCRIPTION,
                                name="control_code",
                                inset_text=False,
                            ),
                        ],
                    ),
                    Option(key="no", value=CreateGoodForm.IsControlled.NO),
                    conditional(not application_pk, Option(key="unsure", value=CreateGoodForm.IsControlled.UNSURE)),
                ],
            ),
            RadioButtons(
                title=CreateGoodForm.IsGraded.TITLE,
                description=CreateGoodForm.IsGraded.DESCRIPTION,
                name="is_pv_graded",
                options=[
                    Option(key="yes", value=CreateGoodForm.IsGraded.YES),
                    Option(key="no", value=CreateGoodForm.IsGraded.NO),
                    conditional(
                        not application_pk, Option(key="grading_required", value=CreateGoodForm.IsGraded.RAISE_QUERY)
                    ),
                ],
            ),
        ],
        back_link=conditional(
            application_pk,
            BackLink(generic.BACK, reverse_lazy("applications:goods", kwargs={"pk": application_pk})),
            Breadcrumbs(
                [
                    BackLink(generic.SERVICE_NAME, reverse_lazy("core:hub")),
                    BackLink(GoodsList.TITLE, reverse_lazy("goods:goods")),
                    BackLink(GoodsList.CREATE_GOOD),
                ]
            ),
        ),
        default_button_name=CreateGoodForm.SUBMIT_BUTTON,
    )


def pv_details_form():
    return Form(
        title=GoodGradingForm.TITLE,
        description=GoodGradingForm.DESCRIPTION,
        questions=[
            Heading("PV grading", HeadingStyle.M),
            Group(
                name="grading",
                components=[
                    TextInput(title=GoodGradingForm.PREFIX, name="prefix", optional=True),
                    Select(
                        options=get_pv_gradings(request=None, convert_to_options=True),
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


def add_good_form_group(is_pv_graded: bool = None, draft_pk: str = None):
    return FormGroup([add_goods_questions(draft_pk), conditional(is_pv_graded, pv_details_form())])


def edit_good_detail_form(good_id):
    return Form(
        title=EditGoodForm.TITLE,
        description=EditGoodForm.DESCRIPTION,
        questions=[
            TextArea(
                title=EditGoodForm.Description.TITLE,
                description=EditGoodForm.Description.DESCRIPTION,
                name="description",
                extras={"max_length": 280},
            ),
            TextInput(title=EditGoodForm.PartNumber.TITLE, name="part_number", optional=True),
            RadioButtons(
                title=EditGoodForm.IsControlled.TITLE,
                description=EditGoodForm.IsControlled.DESCRIPTION,
                name="is_good_controlled",
                options=[
                    Option(
                        key="yes",
                        value=EditGoodForm.IsControlled.YES,
                        components=[
                            control_list_entry_question(
                                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                                title=EditGoodForm.ControlListEntry.TITLE,
                                description=EditGoodForm.ControlListEntry.DESCRIPTION,
                                name="control_code",
                                inset_text=False,
                            ),
                        ],
                    ),
                    Option(key="no", value=EditGoodForm.IsControlled.NO),
                    Option(key="unsure", value=EditGoodForm.IsControlled.UNSURE),
                ],
            ),
            RadioButtons(
                title=CreateGoodForm.IsGraded.TITLE,
                description=CreateGoodForm.IsGraded.DESCRIPTION,
                name="is_pv_graded",
                options=[
                    Option(key="yes", value=CreateGoodForm.IsGraded.YES),
                    Option(key="no", value=CreateGoodForm.IsGraded.NO),
                    Option(key="grading_required", value=CreateGoodForm.IsGraded.RAISE_QUERY),
                ],
            ),
        ],
        buttons=[
            Button(EditGoodForm.Buttons.SAVE, "submit", ButtonStyle.DEFAULT),
            Button(
                value=EditGoodForm.Buttons.DELETE,
                action="",
                style=ButtonStyle.WARNING,
                link=reverse_lazy("goods:delete", kwargs={"pk": good_id}),
                float_right=True,
            ),
        ],
        back_link=BackLink(CreateGoodForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
    )


def edit_good_form_group(good_id, is_pv_graded: bool = None):
    return FormGroup([edit_good_detail_form(good_id), conditional(is_pv_graded, pv_details_form())])


def document_grading_form(request, good_id):
    select_options = get_document_missing_reasons(request)[0]["reasons"]

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
        back_link=BackLink(DocumentSensitivityForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
        default_button_name=DocumentSensitivityForm.SUBMIT_BUTTON,
    )


def attach_documents_form(back_link):
    return Form(
        title=AttachDocumentForm.TITLE,
        description=AttachDocumentForm.DESCRIPTION,
        questions=[
            FileUpload("document"),
            TextArea(
                title=AttachDocumentForm.Description.TITLE,
                optional=True,
                name="description",
                extras={"max_length": 280},
            ),
        ],
        buttons=[Button(AttachDocumentForm.BUTTON, "submit", disable_double_click=True)],
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


def respond_to_query_form(good_id, ecju_query):
    return Form(
        title=RespondToQueryForm.TITLE,
        description="",
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(
                name="response",
                title=RespondToQueryForm.Response.TITLE,
                description=RespondToQueryForm.Response.DESCRIPTION,
                extras={"max_length": 2200},
            ),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(
            RespondToQueryForm.BACK_LINK,
            reverse_lazy("goods:good_detail", kwargs={"pk": good_id, "type": "ecju-queries"}),
        ),
        default_button_name=RespondToQueryForm.BUTTON,
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title=RespondToQueryForm.ConfirmationForm.TITLE,
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label=RespondToQueryForm.ConfirmationForm.YES,
        no_label=RespondToQueryForm.ConfirmationForm.NO,
        back_link_text=RespondToQueryForm.ConfirmationForm.BACK_LINK,
        back_url=edit_response_url,
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
                link=reverse_lazy("goods:edit", kwargs={"pk": good["id"]}),
            ),
        ],
    )
