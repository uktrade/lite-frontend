from django.core.exceptions import ValidationError
import re


def validate_name(value):
    if value:
        match_regex = re.sub(r"[^a-zA-Z0-9 .,\\-\\)\\/'+:=\\?\\!\"%&\\*;\\<\\>]", "", value)
        if len(match_regex) < len(value):
            raise ValidationError("""Invalid character, allowed characters: A-Z a-z 0-9 -()/'+:=?!"_ ."%&*;<>""")
