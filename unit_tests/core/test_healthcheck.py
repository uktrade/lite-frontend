import pytest

from django.test import RequestFactory

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException
from health_check.plugins import plugin_dir

from core.health_check.views import HealthCheckPingdomView


@pytest.fixture(autouse=True)
def backends():
    unaltered_value = plugin_dir._registry
    yield plugin_dir
    plugin_dir._registry = unaltered_value


class HealthCheckOk(BaseHealthCheckBackend):
    def check_status(self):
        return True

    def run_check(self):
        super().run_check()
        self.time_taken = 0.33


class HealthCheckBroken(BaseHealthCheckBackend):
    def check_status(self):
        raise HealthCheckException("error")

    def run_check(self):
        super().run_check()
        self.time_taken = 0.23


def test_healthcheck_ok(backends):
    backends.reset()
    backends.register(HealthCheckOk)
    request = RequestFactory().get("/")
    response = HealthCheckPingdomView.as_view()(request)

    assert response.status_code == 200
    assert response.render().content == (
        b'<?xml version="1.0" encoding="UTF-8"?>'
        b"<pingdom_http_custom_check><status>\n    \n        "
        b"OK\n    \n    "
        b"</status>"
        b"<response_time>0.33</response_time>"
        b"</pingdom_http_custom_check>\n"
    )


def test_healthcheck_down(backends):
    backends.reset()
    backends.register(HealthCheckBroken)
    request = RequestFactory().get("/")
    response = HealthCheckPingdomView.as_view()(request)

    assert response.status_code == 500
    assert response.render().content == (
        b'<?xml version="1.0" encoding="UTF-8"?>'
        b"<pingdom_http_custom_check>"
        b"<status>\n    \n        "
        b"HealthCheckBroken: unknown error: error\n    \n    "
        b"</status><response_time>0.23</response_time>"
        b"</pingdom_http_custom_check>\n"
    )
