from uuid import uuid4

import pytest

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from unit_tests.helpers import reload_urlconf


def lookup_urls():
    reverse("compliance:compliance_list")
    reverse("compliance:compliance_site_details", kwargs={"tab": "foo", "pk": uuid4()})
    reverse("compliance:compliance_visit_details", kwargs={"tab": "foo", "site_case_id": uuid4(), "pk": uuid4()})
    reverse("compliance:open_licence_returns_list")
    reverse("compliance:open_licence_returns_download", kwargs={"pk": uuid4()})
    reverse("compliance:add_open_licence_return")
    reverse("compliance:add_open_licence_return_success", kwargs={"pk": uuid4()})


def test_url_respects_feature_flag_off(settings):
    # given the feature is turned on
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = True
    reload_urlconf(["exporter.compliance.urls", settings.ROOT_URLCONF])

    # when urls are looked up

    # but non SIEL urls are not found
    with pytest.raises(NoReverseMatch):
        lookup_urls()


def test_url_respects_feature_flag_on(settings):
    # given the feature is turned off
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = False
    reload_urlconf(["exporter.compliance.urls", settings.ROOT_URLCONF])

    # when urls are looked up

    # then nothing bad happens
    lookup_urls()
