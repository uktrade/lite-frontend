import rules
from django.conf import settings


@rules.predicate
def can_exporter_use_f680s(request):
    return (
        request.session["organisation"] in settings.FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS
        or settings.FEATURE_FLAG_ALLOW_F680
    )


rules.add_rule(
    "can_exporter_use_f680s",
    can_exporter_use_f680s,
)
