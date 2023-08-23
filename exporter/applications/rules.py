import rules

from datetime import datetime

from django.conf import settings


@rules.predicate
def is_appeal_feature_flag_set(request, application):
    if not settings.FEATURE_FLAG_APPEALS:
        return False

    if application and (application.licence or not application.appeal_deadline):
        return False

    appeal_deadline_date_str = application.appeal_deadline.split("T")[0]
    appeal_deadline = datetime.strptime(appeal_deadline_date_str, "%Y-%m-%d")

    return datetime.today().date() <= appeal_deadline.date()


rules.add_rule("can_user_appeal_case", is_appeal_feature_flag_set)
