import datetime
import pytest
import uuid

from django.db import models

from core.summaries.formatters import (
    add_edit_links,
    add_labels,
    choices_formatter,
    comma_separated_list,
    date_formatter,
    document_formatter,
    format_values,
    identity,
    integer,
    just,
    key_value_formatter,
    mapping_formatter,
    model_choices_formatter,
    money_formatter,
    organisation_document_formatter,
    template_formatter,
    to_date,
    yesno,
)


@pytest.mark.parametrize(
    ("summary,labels,output"),
    (
        (
            (),
            {},
            (),
        ),
        (
            (("summary-key",),),
            {},
            (("summary-key", "summary-key"),),
        ),
        (
            (("summary-key", "rest-1", "rest-2"),),
            {},
            (("summary-key", "rest-1", "rest-2", "summary-key"),),
        ),
        (
            (
                ("summary-key-1",),
                ("summary-key-2",),
                ("summary-key-3",),
            ),
            {
                "summary-key-1": "Summary Label 1",
                "summary-key-2": "Summary Label 2",
                "summary-key-3": "Summary Label 3",
            },
            (
                ("summary-key-1", "Summary Label 1"),
                ("summary-key-2", "Summary Label 2"),
                ("summary-key-3", "Summary Label 3"),
            ),
        ),
        (
            (
                ("summary-key-1", "rest-1", "rest-2"),
                ("summary-key-2", "rest-1", "rest-2"),
                ("summary-key-3", "rest-1", "rest-2"),
            ),
            {
                "summary-key-1": "Summary Label 1",
                "summary-key-2": "Summary Label 2",
                "summary-key-3": "Summary Label 3",
            },
            (
                ("summary-key-1", "rest-1", "rest-2", "Summary Label 1"),
                ("summary-key-2", "rest-1", "rest-2", "Summary Label 2"),
                ("summary-key-3", "rest-1", "rest-2", "Summary Label 3"),
            ),
        ),
    ),
)
def test_add_labels(summary, labels, output):
    assert add_labels(summary, labels) == output


def test_key_value_formatter():
    assert (
        key_value_formatter(
            {
                "key": "a key",
                "value": "a value",
            }
        )
        == "a value"
    )


@pytest.mark.parametrize(
    "value",
    (
        "foo",
        {"foo": "bar"},
        ["foo", "bar", "baz"],
        42,
    ),
)
def test_identity(value):
    assert identity(value) is value


@pytest.mark.parametrize(
    "formatter,value_list,output",
    (
        (
            None,
            ["foo", "bar", "baz"],
            "foo, bar, baz",
        ),
        (
            lambda x: x.upper(),
            ["foo", "bar", "baz"],
            "FOO, BAR, BAZ",
        ),
        (
            None,
            None,
            "",
        ),
    ),
)
def test_comma_separated_list(formatter, value_list, output):
    args = ()
    if formatter:
        args = (formatter,)

    formatter = comma_separated_list(*args)
    assert formatter(value_list) == output


@pytest.mark.parametrize(
    "value,output",
    (
        (True, "Yes"),
        (False, "No"),
    ),
)
def test_yesno(value, output):
    assert yesno(value) == output


def test_to_date():
    assert to_date("2020-10-09") == datetime.date(2020, 10, 9)


@pytest.mark.parametrize(
    "format,value,output",
    (
        (
            None,
            "2020-10-09",
            "9 Oct 2020",
        ),
        (
            "j m Y",
            "2020-10-09",
            "9 10 2020",
        ),
    ),
)
def test_date_formatter(format, value, output):
    args = ()
    if format:
        args = (format,)

    formatter = date_formatter(*args)
    assert formatter(value) == output


@pytest.mark.parametrize(
    "map,value,output",
    (
        (
            {
                "key": "Mapped value",
            },
            "key",
            "Mapped value",
        ),
        (
            {
                "key": "Mapped value",
            },
            "not-a-key",
            "not-a-key",
        ),
    ),
)
def test_mapping_formatter(map, value, output):
    formatter = mapping_formatter(map)
    assert formatter(value) == output


@pytest.mark.parametrize(
    "document,output",
    (
        (
            {
                "id": uuid.uuid4(),
                "document": {
                    "safe": True,
                    "name": "document name",
                },
            },
            '<a class="govuk-link govuk-link--no-visited-state" href="/organisation/document/{pk}/" target="_blank">{name}</a>',
        ),
        (
            {
                "id": uuid.uuid4(),
                "document": {
                    "safe": False,
                    "name": "document name",
                },
            },
            "{name}",
        ),
    ),
)
def test_organisation_document_formatter(document, output):
    output = output.format(
        pk=document["id"],
        name=document["document"]["name"],
    )
    assert organisation_document_formatter(document) == output


def test_format_values():
    summary = (
        ("key", "value"),
        ("not-formatted", "not-formatted"),
    )
    formatters = {
        "key": lambda x: x.upper(),
    }
    assert format_values(summary, formatters) == (
        ("key", "VALUE"),
        ("not-formatted", "not-formatted"),
    )


@pytest.mark.parametrize(
    "document,output",
    (
        (
            {
                "safe": True,
                "name": "document name",
            },
            '<a class="govuk-link govuk-link--no-visited-state" href="{url}" target="_blank">document name</a>',
        ),
        (
            {
                "safe": True,
                "name": "<escape>evil html</escape>",
            },
            '<a class="govuk-link govuk-link--no-visited-state" href="{url}" target="_blank">&lt;escape&gt;evil html&lt;/escape&gt;</a>',
        ),
        (
            {
                "safe": False,
                "name": "document name",
            },
            "document name",
        ),
    ),
)
def test_document_formatter(document, output):
    url = "http://example.com/test"
    assert document_formatter(document, url) == output.format(url=url)


@pytest.mark.parametrize(
    "document,output",
    (
        (
            {
                "safe": True,
                "name": "document name",
            },
            '<a class="govuk-link govuk-link--no-visited-state" href="{url}" target="_blank">overridden text</a>',
        ),
        (
            {
                "safe": False,
                "name": "document name",
            },
            "document name",
        ),
    ),
)
def test_document_formatter_overriden_name(document, output):
    url = "http://example.com/test"
    assert document_formatter(document, url, "overridden text") == output.format(url=url)


def test_just():
    formatter = just("This value")
    assert formatter("something else") == "This value"


@pytest.mark.parametrize(
    "input,output",
    (
        (
            "14",
            "£14.00",
        ),
        ("14.1", "£14.10"),
        ("14.12", "£14.12"),
    ),
)
def test_money_formatter(input, output):
    assert money_formatter(input) == output


class TextChoice(models.TextChoices):
    A = "A", "This is a"
    B = "B", "This is b"
    C = "C", "This is c"


class DifferingNameAndValueTextChoice(models.TextChoices):
    FOO = "different", "foo"
    BAR = "another", "bar"


@pytest.mark.parametrize(
    "choices, input, output",
    (
        (
            (
                (True, "This is the true value"),
                (False, "This is the false value"),
            ),
            True,
            "This is the true value",
        ),
        (
            (
                (True, "This is the true value"),
                (False, "This is the false value"),
            ),
            False,
            "This is the false value",
        ),
        (
            (
                ("foo", "This is the foo value"),
                ("bar", "This is the bar value"),
                ("baz", "This is the foo value"),
            ),
            "foo",
            "This is the foo value",
        ),
    ),
)
def test_choices_formatter(choices, input, output):
    formatter = choices_formatter(choices)
    assert formatter(input) == output


@pytest.mark.parametrize(
    "enum_type,input,output",
    (
        (
            TextChoice,
            TextChoice.A,
            TextChoice.A.label,
        ),
        (
            TextChoice,
            TextChoice.B,
            TextChoice.B.label,
        ),
        (
            TextChoice,
            TextChoice.C,
            TextChoice.C.label,
        ),
        (
            DifferingNameAndValueTextChoice,
            DifferingNameAndValueTextChoice.FOO,
            DifferingNameAndValueTextChoice.FOO.label,
        ),
        (
            DifferingNameAndValueTextChoice,
            DifferingNameAndValueTextChoice.BAR,
            DifferingNameAndValueTextChoice.BAR.label,
        ),
    ),
)
def test_model_choices_formatter(enum_type, input, output):
    formatter = model_choices_formatter(enum_type)
    assert formatter(input) == output


def test_template_formatter():
    formatter = template_formatter("tests/template-formatter.html", lambda val: {"key": val})
    assert formatter("value") == "<p>value</p>\n"


@pytest.mark.parametrize(
    "input,output",
    (
        ("1", "1"),
        (1.0, "1"),
        (1, "1"),
        (1.5, "1"),
    ),
)
def test_integer(input, output):
    assert integer(input) == output


def test_add_edit_links():
    summary = (
        ("has-edit-link", "foo", "bar"),
        ("no-edit-link", "foo", "bar"),
    )
    edit_links = {
        "has-edit-link": "has_edit_link",
    }
    get_edit_link = lambda link: f"http://example.com/{link}/"

    assert add_edit_links(summary, edit_links, get_edit_link) == (
        ("has-edit-link", "foo", "bar", "http://example.com/has_edit_link/"),
        ("no-edit-link", "foo", "bar", None),
    )
