from core.builtins.custom_tags import str_date
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Summary


def draft_summary(draft):
    if not draft:
        return None

    return Summary(
        values={
            strings.applications.ApplicationSummaryPage.REFERENCE_NAME: draft["name"],
            strings.applications.ApplicationSummaryPage.TYPE: draft["case_type"]["sub_type"]["key"],
            strings.applications.ApplicationSummaryPage.CREATED_AT: str_date(draft["created_at"]),
        },
        classes=["govuk-summary-list--no-border"],
    )


def application_summary(application):
    if not application:
        return None

    return Summary(
        values={
            strings.applications.ApplicationSummaryPage.REFERENCE_NAME: application["name"],
            strings.applications.ApplicationSummaryPage.REFERENCE_CODE: application["reference_code"],
            strings.applications.ApplicationSummaryPage.TYPE: application["case_type"]["sub_type"]["key"],
            strings.applications.ApplicationSummaryPage.SUBMITTED_AT: str_date(application["submitted_at"]),
        },
        classes=["govuk-summary-list--no-border"],
    )
