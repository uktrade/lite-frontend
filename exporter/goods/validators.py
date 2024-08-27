from django.core.exceptions import ValidationError
import re


def validate_name(value):
    if value:
        match_regex = re.compile(r"^[a-zA-Z0-9 .,\-\)\(\/'+:=\?\!\"%&\*;\<\>]+$")
        is_value_valid = bool(match_regex.match(value))
        if not is_value_valid:
            raise ValidationError("""Invalid character, allowed characters: A-Z a-z 0-9 -()/'+:=?!" ."%&*;<>""")
