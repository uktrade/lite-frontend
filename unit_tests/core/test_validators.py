import pytest
from django.core.exceptions import ValidationError
from exporter.core.validators import EdifactStringValidator


@pytest.mark.parametrize(
    "value",
    ((""), ("random value"), ("random-value"), ("random!value"), ("random-!.<>/%&*;+'(),.value")),
)
def test_edifactstringvalidator_valid(value):
    validator = EdifactStringValidator()
    result = validator(value)
    assert result == None


@pytest.mark.parametrize("value", (("\r\n"), ("random_value"), ("random$value"), ("random@value")))
def test_edifactstringvalidator_invalid(value):
    validator = EdifactStringValidator()
    with pytest.raises(ValidationError):
        results = validator(value)
