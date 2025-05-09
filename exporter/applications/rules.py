import dateparser
import rules

from datetime import datetime

from django.conf import settings

from exporter.applications.services import get_status_properties
from exporter.applications.constants import ApplicationStatus


@rules.predicate
def is_application_finalised(request, application):
    if not application:
        return False

    return application.status == ApplicationStatus.FINALISED


@rules.predicate
def is_application_refused(request, application):
    if not application:
        return False

    return not application.licence


@rules.predicate
def appeal_within_deadline(request, application):
    if not application:
        return False

    if not application.appeal_deadline:
        return False

    appeal_deadline = dateparser.parse(application.appeal_deadline)
    return appeal_deadline.date() >= datetime.today().date()


@rules.predicate
def is_application_appealed(request, application):
    if not application:
        return False

    return bool(application.appeal)


@rules.predicate
def is_application_in_draft(request, application):
    return application and application.status == ApplicationStatus.DRAFT


@rules.predicate
def is_application_in_major_edit(request, application):
    return application and application.status == ApplicationStatus.APPLICANT_EDITING


@rules.predicate
def can_invoke_major_editable(request, application):
    status_props, _ = get_status_properties(request, application.status)
    return application and status_props["can_invoke_major_editable"]


@rules.predicate
def is_organisation_in_indeterminate_export_licence_type_cohort(request):
    if "*" in settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS:
        return True

    return (
        request.session["organisation"] in settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS
    )


rules.add_rule(
    "can_user_appeal_case",
    is_application_finalised & is_application_refused & appeal_within_deadline & ~is_application_appealed,  # noqa
)

rules.add_rule(
    "can_view_appeal_details",
    is_application_refused & is_application_appealed,
)

rules.add_rule("can_edit_quantity_value", is_application_in_draft | is_application_in_major_edit)  # noqa

rules.add_rule(
    "can_invoke_major_editable",
    can_invoke_major_editable,
)

rules.add_rule(
    "can_exporter_apply_for_indeterminate_export_licence_type",
    is_organisation_in_indeterminate_export_licence_type_cohort,
)
