import pytest

from lite_forms.components import Option, HelpSection

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
