import pytest

from core.summaries.utils import pick_fields


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
