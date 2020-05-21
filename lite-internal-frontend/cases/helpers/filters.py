from core.services import get_control_list_entries, get_countries
from flags.services import get_flags
from lite_content.lite_internal_frontend.cases import CasesListPage
from lite_forms.components import (
    FiltersBar,
    Option,
    AutocompleteInput,
    Checkboxes,
    Select,
    DateInput,
    TextInput,
    TokenBar,
)
from lite_forms.helpers import conditional


SLA_DAYS_RANGE = 99


def case_filters_bar(request, case_data) -> FiltersBar:
    """
    Returns a FiltersBar for the case search page.
    """
    filters = case_data["results"]["filters"]
    statuses = [Option(option["key"], option["value"]) for option in filters["statuses"]]
    case_types = [Option(option["key"], option["value"]) for option in filters["case_types"]]
    gov_users = [Option(option["id"], option["full_name"]) for option in filters["gov_users"]]
    advice_types = [Option(option["key"], option["value"]) for option in filters["advice_types"]]
    sla_sort = [
        Option("ascending", CasesListPage.Filters.SORT_BY_SLA_ELAPSED_ASCENDING),
        Option("descending", CasesListPage.Filters.SORT_BY_SLA_ELAPSED_DESCDENDING),
    ]
    sla_days = [Option(i, i) for i in range(SLA_DAYS_RANGE)]

    return FiltersBar(
        [
            TextInput(name="case_reference", title="case reference"),
            Select(name="case_type", title=CasesListPage.Filters.CASE_TYPE, options=case_types),
            Select(name="status", title=CasesListPage.Filters.CASE_STATUS, options=statuses),
            AutocompleteInput(
                name="case_officer",
                title=CasesListPage.Filters.CASE_OFFICER,
                options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
            ),
            AutocompleteInput(
                name="assigned_user",
                title=CasesListPage.Filters.ASSIGNED_USER,
                options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
            ),
            conditional(
                case_data["results"]["is_work_queue"],
                Checkboxes(
                    name="hidden",
                    options=[Option("true", CasesListPage.Filters.HIDDEN)],
                    classes=["govuk-checkboxes--small"],
                ),
            ),
        ],
        advanced_filters=[
            TextInput(
                name="exporter_application_reference", title=CasesListPage.Filters.EXPORTER_APPLICATION_REFERENCE
            ),
            TextInput(name="organisation_name", title=CasesListPage.Filters.ORGANISATION_NAME),
            TextInput(name="exporter_site_name", title=CasesListPage.Filters.EXPORTER_SITE_NAME),
            TextInput(name="exporter_site_address", title=CasesListPage.Filters.EXPORTER_SITE_ADDRESS),
            Select(name="final_advice_type", title=CasesListPage.Filters.FINAL_ADVICE_TYPE, options=advice_types),
            Select(name="team_advice_type", title=CasesListPage.Filters.TEAM_ADVICE_TYPE, options=advice_types),
            Select(name="max_sla_days_remaining", title=CasesListPage.Filters.MAX_SLA_DAYS_REMAINING, options=sla_days),
            Select(name="min_sla_days_remaining", title=CasesListPage.Filters.MIN_SLA_DAYS_REMAINING, options=sla_days),
            Select(name="sla_days_elapsed", title=CasesListPage.Filters.SLA_DAYS_ELAPSED, options=sla_days),
            Select(
                name="sla_days_elapsed_sort_order", title=CasesListPage.Filters.SORT_BY_SLA_ELAPSED, options=sla_sort
            ),
            DateInput(
                name="submitted_from",
                title=CasesListPage.Filters.SUBMITTED_FROM,
                prefix="submitted_from_",
                inline_title=True,
            ),
            DateInput(
                name="submitted_to", title=CasesListPage.Filters.SUBMITTED_TO, prefix="submitted_to_", inline_title=True
            ),
            DateInput(
                name="finalised_from",
                title=CasesListPage.Filters.FINALISED_FROM,
                prefix="finalised_from_",
                inline_title=True,
            ),
            DateInput(
                name="finalised_to", title=CasesListPage.Filters.FINALISED_TO, prefix="finalised_to_", inline_title=True
            ),
            TextInput(name="party_name", title=CasesListPage.Filters.PARY_NAME),
            TextInput(name="party_address", title=CasesListPage.Filters.PARTY_ADDRESS),
            TextInput(name="goods_related_description", title=CasesListPage.Filters.GOODS_RELATED_DESCRIPTION),
            AutocompleteInput(
                name="country",
                title=CasesListPage.Filters.COUNTRY,
                options=get_countries(request, convert_to_options=True),
            ),
            AutocompleteInput(
                name="control_list_entry",
                title=CasesListPage.Filters.CONTROL_LIST_ENTRY,
                options=get_control_list_entries(request, convert_to_options=True),
            ),
            TokenBar(
                name="flags",
                title=CasesListPage.Filters.FLAGS,
                options=[Option(flag["id"], flag["name"]) for flag in get_flags(request, disable_pagination=True)],
            ),
        ],
    )
