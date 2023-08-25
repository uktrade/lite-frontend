import rules

from django.conf import settings


@rules.predicate
def is_appeal_feature_flag_set(request):
    return settings.FEATURE_FLAG_APPEALS


rules.add_rule("can_user_appeal_case", is_appeal_feature_flag_set)
