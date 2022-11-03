import pytest

from core.summaries.utils import (
    get_field,
    pick_fields,
    pluck_field,
    remove_fields,
)


@pytest.mark.parametrize(
    "summary,fields,output",
    (
        (
            (
                ("reorder-1", "value-1"),
                ("reorder-2", "value-2"),
                ("reorder-3", "value-3"),
            ),
            ["reorder-3", "reorder-2", "reorder-1"],
            (
                ("reorder-3", "value-3"),
                ("reorder-2", "value-2"),
                ("reorder-1", "value-1"),
            ),
        ),
        (
            (
                ("keep-1", "value-1"),
                ("drop-2", "value-2"),
                ("keep-3", "value-3"),
            ),
            ["keep-3", "keep-1"],
            (
                ("keep-3", "value-3"),
                ("keep-1", "value-1"),
            ),
        ),
        (
            (
                ("keep", "value-1"),
                ("drop", "value-2"),
            ),
            ["non-existent", "keep"],
            (("keep", "value-1"),),
        ),
    ),
)
def test_pick_fields(summary, fields, output):
    assert pick_fields(summary, fields) == output


@pytest.mark.parametrize(
    "summary,fields,output",
    (
        (
            (
                ("keep-1", "value-1"),
                ("drop-2", "value-2"),
                ("keep-3", "value-3"),
            ),
            ["drop-2"],
            (
                ("keep-1", "value-1"),
                ("keep-3", "value-3"),
            ),
        ),
        (
            (
                ("keep", "value-1"),
                ("drop", "value-2"),
            ),
            ["non-existent", "drop"],
            (("keep", "value-1"),),
        ),
    ),
)
def test_remove_fields(summary, fields, output):
    assert remove_fields(summary, fields) == output


def test_get_field():
    summary = (
        ("to-get", "value"),
        ("different", "another"),
    )

    got_field = get_field(summary, "to-get")

    assert got_field == ("to-get", "value")


def test_get_field_non_existent_field():
    summary = (("different", "another"),)
    with pytest.raises(KeyError):
        get_field(summary, "to-get")


def test_pluck_field():
    summary = (
        ("to-pluck", "value"),
        ("left-alone", "another"),
    )
    plucked, altered_summary = pluck_field(summary, "to-pluck")

    assert plucked == ("to-pluck", "value")
    assert summary == (
        ("to-pluck", "value"),
        ("left-alone", "another"),
    )
    assert altered_summary == (("left-alone", "another"),)


def test_pluck_non_existent_field():
    summary = (
        ("to-pluck", "value"),
        ("left-alone", "another"),
    )

    with pytest.raises(KeyError):
        pluck_field(summary, "unknown-key")

    assert summary == (
        ("to-pluck", "value"),
        ("left-alone", "another"),
    )
