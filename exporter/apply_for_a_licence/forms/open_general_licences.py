from django.urls import reverse, reverse_lazy

from exporter.apply_for_a_licence.enums import OpenGeneralExportLicenceTypes
from exporter.core.services import (
    get_control_list_entries,
    get_countries,
    get_open_general_licences,
    get_open_general_licence,
)
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import OpenGeneralLicenceQuestions
from lite_content.lite_exporter_frontend.licences import OpenGeneralLicenceRegistration
from lite_forms.components import (
    FormGroup,
    Form,
    AutocompleteInput,
    RadioButtons,
    Option,
    Custom,
    Heading,
    Label,
    Link,
    BackLink,
    WarningBanner,
    HiddenField,
    Button,
    Checkboxes,
)
from lite_forms.generators import success_page
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle
from exporter.organisation.sites.services import get_sites


def no_open_general_licence_form(open_general_licence_type, selected_entry, selected_country):
    return Form(
        title=OpenGeneralLicenceQuestions.NoOpenGeneralLicencesAvailable.TITLE.format(
            open_general_licence_type.name.lower()
        ),
        description=OpenGeneralLicenceQuestions.NoOpenGeneralLicencesAvailable.DESCRIPTION,
        questions=[
            *[
                Label(x.format(open_general_licence_type.name.lower(), selected_entry, selected_country))
                for x in OpenGeneralLicenceQuestions.NoOpenGeneralLicencesAvailable.INFORMATION.split("\n")
            ],
            Link(
                OpenGeneralLicenceQuestions.NoOpenGeneralLicencesAvailable.APPLY_FOR_A_LICENCE_LINK,
                reverse("apply_for_a_licence:start"),
                classes=["govuk-body", "govuk-link--no-visited-state"],
            ),
            Link(
                OpenGeneralLicenceQuestions.NoOpenGeneralLicencesAvailable.RETURN_TO_ACCOUNT_HOME_LINK,
                reverse("core:home"),
                classes=["govuk-body", "govuk-link--no-visited-state"],
            ),
        ],
        buttons=[],
    )


def open_general_licence_forms(request, **kwargs):
    open_general_licence_type = OpenGeneralExportLicenceTypes.get_by_acronym(kwargs["ogl"])
    control_list_entries = get_control_list_entries(request, True)
    countries = get_countries(request, True)
    selected_entry = request.POST.get("control_list_entry")
    selected_country = next((country.value for country in countries if country.key == request.POST.get("country")), "")
    open_general_licences = get_open_general_licences(
        request,
        convert_to_options=True,
        case_type=open_general_licence_type.id,
        control_list_entry=request.POST.get("control_list_entry"),
        country=request.POST.get("country"),
        status="active",
    )
    sites = get_sites(request, request.session["organisation"], True)
    selected_open_general_licence = {}
    if request.POST.get("open_general_licence"):
        selected_open_general_licence = get_open_general_licence(request, request.POST.get("open_general_licence"))

    if open_general_licence_type.acronym == OpenGeneralExportLicenceTypes.open_general_export_licence.acronym:
        back_link_url = reverse("apply_for_a_licence:export_licence_questions")
    elif open_general_licence_type.acronym == OpenGeneralExportLicenceTypes.open_general_transhipment_licence.acronym:
        back_link_url = reverse("apply_for_a_licence:transhipment_questions")
    else:
        back_link_url = reverse("apply_for_a_licence:trade_control_licence_questions")

    return FormGroup(
        [
            Form(
                title=OpenGeneralLicenceQuestions.ControlListEntry.TITLE,
                description=OpenGeneralLicenceQuestions.ControlListEntry.DESCRIPTION,
                questions=[AutocompleteInput(name="control_list_entry", options=control_list_entries)],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(url=back_link_url),
            ),
            Form(
                title=OpenGeneralLicenceQuestions.Country.TITLE,
                description=OpenGeneralLicenceQuestions.Country.DESCRIPTION,
                questions=[AutocompleteInput(name="country", options=countries)],
                default_button_name=generic.CONTINUE,
            ),
            *conditional(
                open_general_licences,
                [
                    Form(
                        title=OpenGeneralLicenceQuestions.OpenGeneralLicences.TITLE.format(
                            open_general_licence_type.name.lower()
                        ),
                        questions=[
                            Label(
                                OpenGeneralLicenceQuestions.OpenGeneralLicences.DESCRIPTION.format(
                                    open_general_licence_type.name.lower(), selected_entry, selected_country
                                )
                            ),
                            Label(OpenGeneralLicenceQuestions.OpenGeneralLicences.HELP_TEXT),
                            RadioButtons(
                                name="open_general_licence",
                                options=[
                                    *open_general_licences,
                                    Option(
                                        "",
                                        OpenGeneralLicenceQuestions.OpenGeneralLicences.NONE_OF_THE_ABOVE,
                                        show_or=True,
                                    ),
                                ],
                            ),
                        ],
                        default_button_name=generic.CONTINUE,
                    )
                ],
                [no_open_general_licence_form(open_general_licence_type, selected_entry, selected_country)],
            ),
            conditional(
                selected_open_general_licence,
                Form(
                    caption=conditional(
                        selected_open_general_licence.get("registration_required"),
                        OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.CAPTION,
                    ),
                    title=open_general_licence_type.name + " (" + selected_open_general_licence.get("name", "") + ")",
                    questions=[
                        conditional(
                            not selected_open_general_licence.get("registration_required"),
                            WarningBanner(
                                "warning",
                                OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.NO_REGISTRATION_REQUIRED.format(
                                    open_general_licence_type.name.lower()
                                ),
                            ),
                        ),
                        HiddenField("application_type", open_general_licence_type.acronym.lower()),
                        *conditional(
                            selected_open_general_licence.get("registration_required"),
                            [
                                Heading(
                                    OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.Summary.HEADING, HeadingStyle.S
                                ),
                                Custom(
                                    "components/ogl-step-list.html",
                                    data={**selected_open_general_licence, "sites": sites},
                                ),
                                Custom("components/ogl-warning.html"),
                                Checkboxes(
                                    name="confirmation[]",
                                    options=[
                                        Option("read", OpenGeneralLicenceQuestions.Conditions.READ),
                                        Option("comply", OpenGeneralLicenceQuestions.Conditions.COMPLY),
                                    ],
                                ),
                            ],
                            [],
                        ),
                    ],
                    buttons=[
                        conditional(
                            selected_open_general_licence.get("registration_required"),
                            Button("Register", "submit"),
                        )
                    ],
                ),
                no_open_general_licence_form(open_general_licence_type, selected_entry, selected_country),
            ),
        ]
    )


def open_general_licence_submit_success_page(request, **kwargs):
    open_general_licence = get_open_general_licence(request, kwargs["pk"])
    return success_page(
        request=request,
        title=OpenGeneralLicenceRegistration.TITLE,
        secondary_title=OpenGeneralLicenceRegistration.SECONDARY_TITLE.format(
            open_general_licence["case_type"]["reference"]["value"], open_general_licence["name"]
        ),
        description="",
        what_happens_next=[],
        includes="includes/open-general-licence.html",
        additional_context={"licence": open_general_licence},
        links={
            OpenGeneralLicenceRegistration.Links.VIEW_OGLS_LINK: reverse_lazy(
                "licences:list-open-and-standard-licences"
            )
            + "?licence_type=open_general_licences",
            OpenGeneralLicenceRegistration.Links.APPLY_AGAIN: reverse_lazy("apply_for_a_licence:start"),
            OpenGeneralLicenceRegistration.Links.RETURN_TO_DASHBOARD: reverse_lazy("core:home"),
        },
    )
