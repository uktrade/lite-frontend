from uuid import uuid4

import pytest

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from unit_tests.helpers import reload_urlconf


def test_url_respects_feature_flag_off(settings):
    # given the feature is turned on
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = True
    reload_urlconf(["exporter.apply_for_a_licence.urls", settings.ROOT_URLCONF])

    # when urls are looked up

    # then SIEL and start url are found
    reverse("apply_for_a_licence:start")
    reverse("apply_for_a_licence:export_licence_questions")

    # but non SIEL urls are not found
    with pytest.raises(NoReverseMatch):
        reverse("apply_for_a_licence:trade_control_licence_questions")
        reverse("apply_for_a_licence:transhipment_questions")
        reverse("apply_for_a_licence:mod_questions")
        reverse("apply_for_a_licence:ogl_questions", kwargs={"ogl": "foo"})
        reverse("apply_for_a_licence:ogl_submit", kwargs={"ogl": "foo", "pk": uuid4()})


def test_url_respects_feature_flag_on(settings):
    # given the feature is not turned on
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = False
    reload_urlconf(["exporter.apply_for_a_licence.urls", settings.ROOT_URLCONF])

    # when urls are looked up

    # then SIEL and start url are found
    reverse("apply_for_a_licence:start")
    reverse("apply_for_a_licence:export_licence_questions")

    # and non SIEL urls are not found
    reverse("apply_for_a_licence:trade_control_licence_questions")
    reverse("apply_for_a_licence:transhipment_questions")
    reverse("apply_for_a_licence:mod_questions")
    reverse("apply_for_a_licence:ogl_questions", kwargs={"ogl": "foo"})
    reverse("apply_for_a_licence:ogl_submit", kwargs={"ogl": "foo", "pk": uuid4()})
