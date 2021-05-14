from django.urls import reverse_lazy

from exporter.applications.forms.edit import told_by_an_official_form, reference_name_form
from exporter.core.constants import STANDARD
from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.applications import ApplicationSuccessPage
from lite_forms.components import (
    HiddenField,
    Form,
    BackLink,
    TextArea,
    HTMLBlock,
    RadioButtons,
    Option,
    FormGroup,
    TextInput,
    DateInput,
    Label,
    List,
    Link,
    Checkboxes,
)
from lite_forms.generators import success_page
from lite_forms.helpers import conditional


def edit_type_form(application_id):
    return Form(
        title=strings.Applications.Edit.TITLE,
        description=strings.Applications.Edit.DESCRIPTION,
        questions=[
            RadioButtons(
                name="edit-type",
                options=[
                    Option(
                        key="minor",
                        value=strings.Applications.Edit.Minor.TITLE,
                        description=strings.Applications.Edit.Minor.DESCRIPTION,
                    ),
                    Option(
                        key="major",
                        value=strings.Applications.Edit.Major.TITLE,
                        description=strings.Applications.Edit.Major.DESCRIPTION,
                    ),
                ],
            )
        ],
        back_link=BackLink(
            strings.BACK_TO_APPLICATION, reverse_lazy("applications:application", kwargs={"pk": application_id}),
        ),
        default_button_name=strings.CONTINUE,
    )


def application_success_page(request, application_reference_code):
    return success_page(
        request=request,
        title=ApplicationSuccessPage.TITLE,
        secondary_title=ApplicationSuccessPage.SECONDARY_TITLE + application_reference_code,
        description=ApplicationSuccessPage.DESCRIPTION,
        what_happens_next=ApplicationSuccessPage.WHAT_HAPPENS_NEXT,
        links={
            ApplicationSuccessPage.VIEW_APPLICATIONS: reverse_lazy("applications:applications"),
            ApplicationSuccessPage.APPLY_AGAIN: reverse_lazy("apply_for_a_licence:start"),
            ApplicationSuccessPage.RETURN_TO_DASHBOARD: reverse_lazy("core:home"),
        },
    )


def application_copy_form(application_type=None):
    return FormGroup(
        forms=[reference_name_form(), conditional((application_type == STANDARD), told_by_an_official_form()),]
    )


def exhibition_details_form(application_id):
    return Form(
        title=strings.Exhibition.EXHIBITION_TITLE,
        questions=[
            TextInput(title=strings.Exhibition.TITLE, name="title"),
            DateInput(
                title=strings.Exhibition.FIRST_EXHIBITION_DATE,
                description=strings.Exhibition.DATE_DESCRIPTION,
                prefix="first_exhibition_date",
                name="first_exhibition_date",
            ),
            DateInput(
                title=strings.Exhibition.REQUIRED_BY_DATE,
                description=strings.Exhibition.DATE_DESCRIPTION,
                prefix="required_by_date",
                name="required_by_date",
            ),
            TextArea(
                title=strings.Exhibition.REASON_FOR_CLEARANCE,
                name="reason_for_clearance",
                optional=True,
                extras={"max_length": 2000},
            ),
        ],
        back_link=BackLink(
            strings.BACK_TO_APPLICATION, reverse_lazy("applications:task_list", kwargs={"pk": application_id}),
        ),
    )


def declaration_form(application_id):
    return Form(
        title=strings.declaration.Declaration.TITLE,
        questions=[
            HiddenField(name="submit_declaration", value=True),
            # Terms and conditions
            Label("<b>" + strings.declaration.TermsAndConditions.TITLE + "</b>"),
            Label(strings.declaration.TermsAndConditions.PARAGRAPH_ONE),
            Label(strings.declaration.TermsAndConditions.PARAGRAPH_TWO),
            # Licence conditions
            Label("<b>" + strings.declaration.LicenceConditions.TITLE + "<b>"),
            # Authorisation
            Label("<u>" + strings.declaration.LicenceConditions.Authorisation.TITLE + "</u>"),
            Label(strings.declaration.LicenceConditions.Authorisation.PARAGRAPH_ONE),
            HTMLBlock(
                "<ol class='govuk-list govuk-list--number'>"
                "<ol type='a'>"
                "<li>" + strings.declaration.LicenceConditions.Authorisation.OPTION_A + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Authorisation.OPTION_B + "</li>"
                "</ol>"
                "</ol>"
            ),
            Label(strings.declaration.LicenceConditions.Authorisation.PARAGRAPH_TWO),
            # Conditions
            Label("<u>" + strings.declaration.LicenceConditions.Conditions.TITLE + "</u>"),
            HTMLBlock(
                "<ol class='govuk-list govuk-list--number'>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_ONE + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_TWO + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_THREE + "<ol type='a'>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_THREE_A + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_THREE_B + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_THREE_C + "</li>"
                "</ol>"
                "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FOUR + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE + "<ol type='a'>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_A + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_B + "<ol type='i'>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_B_I + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_B_II + "</li>"
                "</ol>"
                "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_C + "<ol type='i'>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_C_I + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_C_II + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_C_III + "</li>"
                "</ol>"
                "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_FIVE_D + "</li>"
                "</ol>"
                "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_SIX + "</li>"
                "<li>" + strings.declaration.LicenceConditions.Conditions.LIST_ITEM_SEVEN + "</li>"
                "</ol>"
            ),
            # Standard conditions
            Label("<u>" + strings.declaration.LicenceConditions.StandardConditions.TITLE + "</u>"),
            List(strings.declaration.LicenceConditions.StandardConditions.BULLET_POINTS, type=List.ListType.NUMBERED,),
            # General notes
            Label("<u>" + strings.declaration.LicenceConditions.GeneralNotes.TITLE + "</u>"),
            Label(strings.declaration.LicenceConditions.GeneralNotes.LINK_TEXT),
            Link(
                name="general-notes-link",
                text=strings.declaration.LicenceConditions.GeneralNotes.LINK,
                address=strings.declaration.LicenceConditions.GeneralNotes.LINK,
            ),
            Label(strings.declaration.LicenceConditions.GeneralNotes.PARAGRAPH_ONE),
            Label(strings.declaration.LicenceConditions.GeneralNotes.PARAGRAPH_TWO),
            Label(strings.declaration.LicenceConditions.GeneralNotes.PARAGRAPH_THREE),
            # Declaration
            Label("<strong>" + strings.declaration.Declaration.TITLE + "</strong>"),
            Label(strings.declaration.Declaration.PARAGRAPH_ONE),
            Label(strings.declaration.Declaration.PARAGRAPH_TWO),
            Label(strings.declaration.Declaration.PARAGRAPH_THREE),
            Label(strings.declaration.Declaration.PARAGRAPH_FOUR),
            Checkboxes(
                name="agreed_to_foi",
                options=[Option(key="True", value=strings.declaration.FOI.INFORMATION_DISCLOSURE_TITLE,),],
                classes=["govuk-checkboxes--small"],
            ),
            TextArea(title=strings.declaration.FOI.INFORMATION_DISCLOSURE_DETAILS, name="foi_reason",),
            Label(strings.declaration.Declaration.FOI_MORE_ADVICE),
            Label(strings.declaration.Declaration.FOI_GUIDANCE),
            TextInput(
                title="Confirm that you agree to the above by typing 'I AGREE' in this box",
                name="agreed_to_declaration_text",
            ),
            Label(
                """Please note, your application must be checked thoroughly and only say 'I agree' if you are content
                that the ELA is accurate. It may not be possible to make changes to the application after
                it has been submitted and if so, you may have to reapply."""
            ),
        ],
        default_button_name=strings.declaration.Declaration.BUTTON_TITLE,
        back_link=BackLink(
            strings.declaration.Declaration.BACK, reverse_lazy("applications:summary", kwargs={"pk": application_id}),
        ),
        javascript_imports={"/javascripts/declaration.js"},
    )
