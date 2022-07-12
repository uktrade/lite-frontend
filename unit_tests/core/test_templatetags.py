import pytest

from django.template import RequestContext, Template


@pytest.mark.parametrize(
    "firearm_details, output",
    (
        ({}, "no"),
        ({"serial_numbers_available": "NOT_AVAILABLE"}, "no"),
        ({"serial_numbers_available": "AVAILABLE"}, "no"),
        ({"serial_numbers_available": "LATER"}, "no"),
        ({"serial_numbers_available": "AVAILABLE", "serial_numbers": []}, "no"),
        ({"serial_numbers_available": "LATER", "serial_numbers": []}, "no"),
        ({"serial_numbers_available": "AVAILABLE", "serial_numbers": ["1111", "2222"]}, "yes"),
        ({"serial_numbers_available": "LATER", "serial_numbers": ["1111", "2222"]}, "yes"),
    ),
)
def test_has_added_serial_numbers(rf, firearm_details, output):
    request = rf.get("/")
    request.session = {}

    t = Template(
        "{% load firearm_details %}{% if firearm_details|has_added_serial_numbers %}yes{% else %}no{% endif %}"
    )
    c = RequestContext(
        request,
        {"firearm_details": firearm_details},
    )
    rendered = t.render(c)

    assert rendered == output


@pytest.mark.parametrize(
    "input, expected",
    (
        ([], ""),
        (["test"], "test"),
        (["test1", "test2"], "test1 and test2"),
        (["test1", "test2", "test3"], "test1, test2 and test3"),
    ),
)
def test_humanise_list(rf, input, expected):
    request = rf.get("/")
    request.session = {}

    t = Template("{{ a_list|humanise_list }}")
    c = RequestContext(
        request,
        {"a_list": input},
    )
    rendered = t.render(c)
    assert rendered == expected
