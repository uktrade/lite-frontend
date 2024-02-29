from django import forms

from core.common.forms import BaseForm


class LoginForm(BaseForm):
    class Layout:
        TITLE = "Mock SSO Login"

    email = forms.CharField()

    def get_layout_fields(self):
        return [
            "email",
        ]
