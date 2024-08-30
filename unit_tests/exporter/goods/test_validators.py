import pytest

from django.core.exceptions import ValidationError

from exporter.goods.validators import validate_name


@pytest.mark.parametrize(
    "name",
    (("random good"), ("good-name"), ("good!name"), ("good-!.<>/%&*;+'(),.name")),
)
def test_validate_goods_name_valid(name):
    assert validate_name(name) is None


@pytest.mark.parametrize("name", (("\r\n"), ("good_name"), ("good$name"), ("good@name")))
def test_validate_goods_name_invalid(name):
    with pytest.raises(ValidationError):
        validate_name(name)
