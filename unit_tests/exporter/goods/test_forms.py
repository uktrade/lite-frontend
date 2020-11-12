import pytest

from lite_forms.components import HelpSection

from exporter.applications.services import serialize_good_on_app_data
from exporter.goods import forms


def test_add_goods_questions_feature_flag_on(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = True

    form = forms.add_goods_questions(control_list_entries=[])

    assert form.questions[2].options[-1].components[0].__class__ == HelpSection
    assert form.questions[3].options[-1].components[0].__class__ == HelpSection


def test_add_goods_questions_feature_flag_off(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = False

    form = forms.add_goods_questions(control_list_entries=[])

    assert form.questions[2].options[-1].components == []
    assert form.questions[3].options[-1].components == []


@pytest.mark.parametrize(
    "value, serialized",
    [
        ("2,300.00", "2300.00"),
        ("2,3,,,,,00.00", "2300.00"),
        ("23,444200", "23444200"),
        ("foo", "foo"),  # this will be caught by serializer on the api and return an error
        ("84.34.111", "84.34.111"),  # this too
    ],
)
def test_serialize_good_on_app_data(value, serialized):
    data = {
        "good_id": "some-uuid",
        "value": value,
    }
    expected = {
        "good_id": "some-uuid",
        "value": serialized,
    }
    assert serialize_good_on_app_data(data) == expected
