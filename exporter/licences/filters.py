from exporter.apply_for_a_licence.enums import OpenGeneralExportLicenceTypes
from lite_content.lite_exporter_frontend.licences import LicencesList, OpenGeneralLicencesList
from lite_forms.components import (
    FiltersBar,
    TextInput,
    HiddenField,
    Select,
    Checkboxes,
    Option,
    AutocompleteInput,
)


def get_licences_filters(licence_type, control_list_entries, countries):
    return FiltersBar(
        [
            TextInput(
                name="reference",
                title=LicencesList.Filters.REFERENCE,
            ),
            AutocompleteInput(
                name="clc",
                title=LicencesList.Filters.CLC,
                options=control_list_entries,
            ),
            AutocompleteInput(
                name="country",
                title=LicencesList.Filters.DESTINATION_COUNTRY,
                options=countries,
            ),
            TextInput(
                name="end_user",
                title=LicencesList.Filters.DESTINATION_NAME,
            ),
            Checkboxes(
                name="active_only",
                options=[Option(key=True, value=LicencesList.Filters.ACTIVE)],
                classes=["govuk-checkboxes--small"],
            ),
            HiddenField(name="licence_type", value=licence_type),
        ]
    )


def get_no_licence_required_filters(licence_type, control_list_entries, countries):
    return FiltersBar(
        [
            TextInput(
                name="reference",
                title=LicencesList.Filters.REFERENCE,
            ),
            AutocompleteInput(
                name="clc",
                title=LicencesList.Filters.CLC,
                options=control_list_entries,
            ),
            AutocompleteInput(
                name="country",
                title=LicencesList.Filters.DESTINATION_COUNTRY,
                options=countries,
            ),
            TextInput(
                name="end_user",
                title=LicencesList.Filters.DESTINATION_NAME,
            ),
            HiddenField(name="licence_type", value=licence_type),
        ]
    )


def get_open_general_licences_filters(licence_type, control_list_entries, countries, sites):
    return FiltersBar(
        [
            TextInput(name="name", title=OpenGeneralLicencesList.Filters.NAME),
            Select(
                name="case_type",
                title=OpenGeneralLicencesList.Filters.TYPE,
                options=OpenGeneralExportLicenceTypes.as_options(),
            ),
            AutocompleteInput(
                name="control_list_entry",
                title=OpenGeneralLicencesList.Filters.CONTROL_LIST_ENTRY,
                options=control_list_entries,
            ),
            AutocompleteInput(name="country", title=OpenGeneralLicencesList.Filters.COUNTRY, options=countries),
            Select(
                name="site",
                title=OpenGeneralLicencesList.Filters.SITE,
                options=sites,
            ),
            Checkboxes(
                name="active_only",
                options=[Option(key=True, value=OpenGeneralLicencesList.Filters.ONLY_SHOW_ACTIVE)],
                classes=["govuk-checkboxes--small"],
            ),
            HiddenField(name="licence_type", value=licence_type),
        ]
    )
