import datetime
import pytest

from core.builtins import custom_tags
from core.builtins.custom_tags import highlight_text
from exporter.core import constants
from exporter.core.objects import Application


@pytest.fixture()
def dummy_choice():
    class FakeType:
        choices = (
            ("T1", "label 1"),
            ("T2", "label 2"),
        )

    return FakeType


@pytest.mark.parametrize(
    "application,expected",
    [
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.STANDARD}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    "is_suspected_wmd": True,
                    "is_eu_military": True,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.STANDARD}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": False,
                    "is_informed_wmd": False,
                    "is_suspected_wmd": False,
                    "is_eu_military": False,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.STANDARD}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    "is_suspected_wmd": True,
                    # missing "is_eu_military"
                }
            ),
            constants.IN_PROGRESS,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.STANDARD}},
                }
            ),
            constants.NOT_STARTED,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.OPEN}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    "is_suspected_wmd": True,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.OPEN}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": False,
                    "is_informed_wmd": False,
                    "is_suspected_wmd": False,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.OPEN}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    # missing "is_suspected_wmd"
                }
            ),
            constants.IN_PROGRESS,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.OPEN}},
                }
            ),
            constants.NOT_STARTED,
        ),
    ],
)
def test_get_end_use_details_status(application, expected):
    assert custom_tags.get_end_use_details_status(application) == expected


@pytest.mark.parametrize(
    "good_on_app,quantity_display",
    [
        ({"quantity": 0, "unit": {"key": "NAR", "value": "Items"}}, "0 items"),
        ({"quantity": 1, "unit": {"key": "NAR", "value": "Items"}}, "1 item"),
        ({"quantity": 2, "unit": {"key": "NAR", "value": "Items"}}, "2 items"),
        ({"quantity": 0.0, "unit": {"key": "NAR", "value": "Items"}}, "0 items"),
        ({"quantity": 1.0, "unit": {"key": "NAR", "value": "Items"}}, "1 item"),
        ({"quantity": 2.0, "unit": {"key": "NAR", "value": "Items"}}, "2 items"),
        ({"quantity": 0, "unit": {"key": "TON", "value": "Tonnes"}}, "0 tonnes"),
        ({"quantity": 1, "unit": {"key": "TON", "value": "Tonnes"}}, "1 tonne"),
        ({"quantity": 2, "unit": {"key": "TON", "value": "Tonnes"}}, "2 tonnes"),
        ({"quantity": 0.0, "unit": {"key": "TON", "value": "Tonnes"}}, "0.0 tonnes"),
        ({"quantity": 1.0, "unit": {"key": "TON", "value": "Tonnes"}}, "1.0 tonne"),
        ({"quantity": 1.5, "unit": {"key": "TON", "value": "Tonnes"}}, "1.5 tonnes"),
        ({"quantity": 2.0, "unit": {"key": "TON", "value": "Tonnes"}}, "2.0 tonnes"),
    ],
)
def test_pluralise_quantity(good_on_app, quantity_display):
    actual = custom_tags.pluralise_quantity(good_on_app)
    assert actual == quantity_display


@pytest.mark.parametrize(
    "input,term,expected",
    [
        ("abc", "notmatch", "abc"),
        ("abc", "bc", 'a<mark class="lite-highlight">bc</mark>'),
        ("<script>", "notmatch", "&lt;script&gt;"),
        ("<script>", "pt", '&lt;scri<mark class="lite-highlight">pt</mark>&gt;'),
        ("<mark>hello", "mark", '&lt;<mark class="lite-highlight">mark</mark>&gt;hello'),
        ("abbbba", "a", '<mark class="lite-highlight">a</mark>bbbb<mark class="lite-highlight">a</mark>'),
    ],
)
def test_highlight_text_sanitization(input, term, expected):
    assert expected == highlight_text(input, term)


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("testfile.pdf", "pdf"),
        ("test file.pdf", "pdf"),
        ("this is test file.pdf", "pdf"),
        ("this-is-a-test-file.docx", "docx"),
        ("test-123_file.doc", "doc"),
        ("testfile.ppt", "ppt"),
        ("testfile", ""),
        ("test_archive.zip", "zip"),
        ("test_archive.tar", "tar"),
        ("test_archive.tar.gz", "gz"),
    ],
)
def test_document_extension(filename, expected):
    assert expected == custom_tags.document_extension(filename)


@pytest.mark.parametrize(
    "date_string,output",
    [
        (None, ""),
        ("2020-08-03T12:52:38.239382", datetime.datetime(2020, 8, 3, 12, 52, 38, 239382)),
        (
            "2020-08-03T12:52:38.239382Z",
            datetime.datetime(2020, 8, 3, 12, 52, 38, 239382, tzinfo=datetime.timezone.utc),
        ),
    ],
)
def test_to_datetime(date_string, output):
    assert custom_tags.to_datetime(date_string) == output


@pytest.mark.parametrize(
    "num1,num2,expected",
    [
        (0, 2, 0),
        (-2, 2, -4),
        (4, 2, 8),
        (1.25, 4, 5.0),
    ],
)
def test_multiply(num1, num2, expected):
    assert expected == custom_tags.multiply(num1, num2)


@pytest.mark.parametrize(
    "num1,num2,expected",
    [
        (0, 2, -2),
        (-2, 2, -4),
        (4, 2, 2),
        (1.25, 4, -2.75),
    ],
)
def test_subtract(num1, num2, expected):
    assert expected == custom_tags.subtract(num1, num2)


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {
                "address": {
                    "country": {"name": "US"},
                    "address_line_1": "42",
                    "address_line_2": "Bakers street",
                    "city": "San Jose",
                    "region": "California",
                    "postcode": "42551",
                }
            },
            "42, Bakers street, San Jose, California, 42551, US",
        ),
        (
            {"address": "54, Bakers street, San Diego, California, 42551", "country": {"name": "United States"}},
            "54, Bakers street, San Diego, California, 42551, United States",
        ),
        (
            {
                "address": "54, Bakers street, San Diego, California, 42551",
            },
            "54, Bakers street, San Diego, California, 42551",
        ),
    ],
)
def test_get_address(data, expected):
    assert expected == custom_tags.get_address(data)


@pytest.mark.parametrize(
    "data,expected",
    [
        ({"first_name": "Internal", "last_name": "User", "email": "user@gov.uk"}, "Internal User"),
        ({"first_name": "", "email": "user@gov.uk"}, "user@gov.uk"),
    ],
)
def test_username(data, expected):
    assert expected == custom_tags.username(data)


@pytest.mark.parametrize(
    "party_type,expected",
    [
        ({"type": "end_user"}, "End User"),
        ({"type": "third_party"}, "Third Party"),
        ({"type": "ultimate_end_user"}, "Ultimate End User"),
        ({"type": "consignee"}, "Consignee"),
    ],
)
def test_get_party_type(party_type, expected):
    assert expected == custom_tags.get_party_type(party_type)


@pytest.mark.parametrize(
    "items, expected",
    [
        ([], ""),
        (None, ""),
        (["T1"], "label 1"),
        (["T1", "T2"], "label 1, label 2"),
    ],
)
def test_list_to_choice_labels(items, expected, dummy_choice):
    assert expected == custom_tags.list_to_choice_labels(items, dummy_choice)
