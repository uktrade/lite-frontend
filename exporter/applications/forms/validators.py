from django.core.exceptions import ValidationError

from exporter.applications.forms.constants import Validation


def validate_name(value):
    if value:
        max_length = Validation.END_USER_NAME_MAX_LENGTH
        if len(value) > max_length:
            raise ValidationError(f'End user name should be {max_length} characters or less')
