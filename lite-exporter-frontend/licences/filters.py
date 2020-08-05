from core.services import get_control_list_entries, get_countries
from lite_content.lite_exporter_frontend.licences import LicencesList
from lite_forms.components import TextInput, AutocompleteInput, Checkboxes, Option


def licences_filters(request):
    return [
        TextInput(name="reference", title=LicencesList.Filters.REFERENCE,),
        AutocompleteInput(
            name="clc",
            title=LicencesList.Filters.CLC,
            options=get_control_list_entries(request, convert_to_options=True),
        ),
        AutocompleteInput(
            name="country",
            title=LicencesList.Filters.DESTINATION_COUNTRY,
            options=get_countries(request, convert_to_options=True),
        ),
        TextInput(name="end_user", title=LicencesList.Filters.DESTINATION_NAME,),
        Checkboxes(
            name="active_only",
            options=[Option(key=True, value=LicencesList.Filters.ACTIVE)],
            classes=["govuk-checkboxes--small"],
        ),
    ]
