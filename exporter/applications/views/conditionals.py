from django.conf import settings


def is_indeterminate_export_licence_type_allowed(wizard):
    return wizard.get_organisation() in settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS
