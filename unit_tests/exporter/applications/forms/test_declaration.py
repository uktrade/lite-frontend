import pytest

from exporter.applications.forms.declaration import ApplicationDeclarationForm


@pytest.mark.parametrize(
    ("data", "is_valid", "errors"),
    [
        ({"agreed_to_foi": False, "foi_reason": None}, True, {}),
        ({"agreed_to_foi": False, "foi_reason": ""}, True, {}),
        ({"agreed_to_foi": False}, True, {}),
        (
            {"agreed_to_foi": True, "foi_reason": None},
            False,
            {"foi_reason": ["Explain why the disclosure of information would be harmful to your interests"]},
        ),
        (
            {"agreed_to_foi": True, "foi_reason": ""},
            False,
            {"foi_reason": ["Explain why the disclosure of information would be harmful to your interests"]},
        ),
        (
            {"agreed_to_foi": True},
            False,
            {"foi_reason": ["Explain why the disclosure of information would be harmful to your interests"]},
        ),
        ({"agreed_to_foi": True, "foi_reason": "I have reasons"}, True, {}),
    ],
)
def test_declaration_form(data, is_valid, errors):
    form = ApplicationDeclarationForm(data=data)
    assert form.is_valid() is is_valid
    assert form.errors == errors
