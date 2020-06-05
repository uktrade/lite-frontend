from django.urls import reverse

from apply_for_a_licence.enums import OpenGeneralExportLicenceTypes
from core.services import get_control_list_entries, get_countries, get_open_general_licences, get_open_general_licence
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import OpenGeneralLicenceQuestions
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
    Summary,
    BackLink,
    WarningBanner,
)
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle


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
    )
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
                        description=OpenGeneralLicenceQuestions.OpenGeneralLicences.DESCRIPTION.format(
                            open_general_licence_type.name.lower(), selected_entry, selected_country
                        ),
                        questions=[
                            RadioButtons(
                                name="open_general_licence",
                                description=OpenGeneralLicenceQuestions.OpenGeneralLicences.HELP_TEXT,
                                options=[
                                    *open_general_licences,
                                    Option(
                                        "",
                                        OpenGeneralLicenceQuestions.OpenGeneralLicences.NONE_OF_THE_ABOVE,
                                        show_or=True,
                                    ),
                                ],
                            )
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
                        Summary(
                            {
                                OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.Summary.DESCRIPTION: selected_open_general_licence.get(
                                    "description"
                                ),
                                OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.Summary.CONTROL_LIST_ENTRIES: ", ".join(
                                    [x["rating"] for x in selected_open_general_licence.get("control_list_entries", [])]
                                ),
                                OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.Summary.COUNTRIES: ", ".join(
                                    [x["name"] for x in selected_open_general_licence.get("countries", [])]
                                ),
                                OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.Summary.READ_MORE_LINK: "["
                                + selected_open_general_licence.get("url", "")
                                + "]("
                                + selected_open_general_licence.get("url", "")
                                + ")",
                            }
                        ),
                        *conditional(
                            selected_open_general_licence.get("registration_required"),
                            [
                                Heading(
                                    OpenGeneralLicenceQuestions.OpenGeneralLicenceDetail.Summary.HEADING, HeadingStyle.S
                                ),
                                Custom("components/ogl-step-list.html"),
                                Custom("components/ogl-warning.html"),
                            ],
                            [],
                        ),
                    ],
                    # Submit button removed as it doesn't do anything until LT-2110
                    buttons=[],
                ),
                no_open_general_licence_form(open_general_licence_type, selected_entry, selected_country),
            ),
        ]
    )
