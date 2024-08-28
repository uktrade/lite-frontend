from django.core.exceptions import ValidationError
import re


def validate_name(value):
    if value:
        match_regex = re.compile(r"^[a-zA-Z0-9 .,\-\)\(\/'+:=\?\!\"%&\*;\<\>]+$")
        is_value_valid = bool(match_regex.match(value))
        if not is_value_valid:
            raise ValidationError(
                "Product name must only include letters, numbers, and common special characters such as hyphens, brackets and apostrophes"
            )
