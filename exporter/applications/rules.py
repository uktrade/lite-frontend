import rules

from datetime import datetime

from django.conf import settings


@rules.predicate
def is_appeal_feature_flag_set(request, application):
    return settings.FEATURE_FLAG_APPEALS


@rules.predicate
def is_application_finalised(request, application):
    if not application:
        return False

    return application.status == "finalised"


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

    appeal_deadline = datetime.fromisoformat(application.appeal_deadline)
    return appeal_deadline.date() >= datetime.today().date()


@rules.predicate
def is_application_appealed(request, application):
    if not application:
        return False

    return bool(application.appeal)


rules.add_rule(
    "can_user_appeal_case",
    is_appeal_feature_flag_set & is_application_finalised & is_application_refused & appeal_within_deadline,
)

rules.add_rule(
    "can_view_appeal_details",
    is_appeal_feature_flag_set & is_application_refused & is_application_appealed,
)
