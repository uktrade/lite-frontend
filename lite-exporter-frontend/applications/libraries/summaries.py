from core.builtins.custom_tags import str_date
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Summary


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
