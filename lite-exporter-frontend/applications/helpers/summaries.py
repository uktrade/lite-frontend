from core.builtins.custom_tags import str_date
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Summary


def draft_summary(draft):
    if not draft:
        return None

    return Summary(
        values={
            strings.APPLICATION_REFERENCE_NAME: draft["name"],
            strings.APPLICATION_TYPE: draft["application_type"]["value"],
            strings.APPLICATION_EXPORT_TYPE: draft["export_type"]["value"],
            strings.APPLICATION_CREATED_AT: str_date(draft["created"]),
        },
        classes=["govuk-summary-list--no-border"],
    )


def application_summary(application):
    if not application:
        return None

    return Summary(
        values={
            strings.APPLICATION_REFERENCE_NAME: application["name"],
            strings.APPLICATION_TYPE: application["application_type"]["value"],
            strings.APPLICATION_EXPORT_TYPE: application["export_type"]["value"],
            strings.APPLICATION_SUBMITTED_AT: str_date(application["submitted_at"]),
        },
        classes=["govuk-summary-list--no-border"],
    )
