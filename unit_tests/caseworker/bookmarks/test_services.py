import datetime
import pytest
import requests
import uuid

from decimal import Decimal

from crispy_forms_gds.fields import DateInputField
from django import forms
from django.urls import reverse

from caseworker.bookmarks.services import enrich_filter_for_saving, BookmarkEnricher
from unit_tests.caseworker.conftest import GOV_USER_ID


def new_bookmarks(filter):
    return [{"name": "Name", "description": "", "filter_json": filter, "id": uuid.uuid4()}]


@pytest.fixture()
def all_cles(data_control_list_entries):
    return data_control_list_entries["control_list_entries"]


@pytest.fixture()
def all_regimes(data_regime_entries):
    return [{"id": regime["pk"], "name": regime["name"]} for regime in data_regime_entries]


@pytest.fixture()
def request_with_session(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    return request


@pytest.fixture()
def mock_form_provider():
    class MockForm(forms.Form):
        case_reference = forms.CharField(
            label="Case reference",
            widget=forms.TextInput(attrs={"id": "case_reference"}),
            required=False,
        )
        submitted_from = DateInputField(
            label="Submitted after",
            required=False,
        )
        submitted_to = DateInputField(
            label="Submitted before",
            required=False,
        )
        finalised_from = DateInputField(
            label="Finalised after",
            required=False,
        )
        finalised_to = DateInputField(
            label="Finalised before",
            required=False,
        )
        is_trigger_list = forms.BooleanField(
            label="Trigger list",
            required=False,
        )
        max_total_value = forms.DecimalField(
            label="Max total value (£)",
            required=False,
            widget=forms.TextInput,
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields["status"] = forms.ChoiceField(
                choices=[("ogd_advice", "OGD Advice")],
                label="Case status",
                required=False,
            )
            self.fields["case_officer"] = forms.ChoiceField(
                choices=[(GOV_USER_ID, "John Smith")],
                label="Licensing Unit case officer",
                widget=forms.Select(attrs={"id": "case_officer"}),
                required=False,
            )
            self.fields["assigned_user"] = forms.ChoiceField(
                choices=[(GOV_USER_ID, "John Smith")],
                label="Case adviser",
                widget=forms.Select(attrs={"id": "case_adviser"}),
                required=False,
            )
            self.fields["control_list_entry"] = forms.MultipleChoiceField(
                label="Control list entry",
                choices=[("ML1", "ML1"), ("ML1a", "ML1a")],
                required=False,
                # setting id for javascript to use
                widget=forms.SelectMultiple(attrs={"id": "control_list_entry"}),
            )
            self.fields["countries"] = forms.MultipleChoiceField(
                label="Country",
                choices=[("DE", "Germany")],
                required=False,
                # setting id for javascript to use
                widget=forms.SelectMultiple(attrs={"id": "countries"}),
            )
            self.fields["regime_entry"] = forms.MultipleChoiceField(
                label="Regime entry",
                choices=[
                    ("d73d0273-ef94-4951-9c51-c291eba949a0", "wassenaar-1"),  # /PS-IGNORE
                    ("c760976f-fd14-4356-9f23-f6eaf084475d", "mtcr-1"),  # /PS-IGNORE
                ],
                required=False,
                # setting id for javascript to use
                widget=forms.SelectMultiple(attrs={"id": "regime_entry"}),
            )
            flag_url = reverse("flags:flags")
            self.fields["flags"] = forms.MultipleChoiceField(
                label="Flags",
                choices=[
                    ("798d5e92-c31a-48cc-9e6b-d3fc6dfd65f2", "BAE"),
                    ("e50f5cd3-331c-4914-b618-ee6eb67a081c", "AG Review Required"),
                ],
                required=False,
                help_text=f'<a href="{flag_url}" class="govuk-link govuk-link--no-visited-state" target="_blank">Flag information (open in a new window)</a>',
                # setting id for javascript to use
                widget=forms.SelectMultiple(attrs={"id": "flags"}),
            )

    class MockFormProvider:
        def get_bound_bookmark_form(self, form_data):
            return MockForm(data=form_data)

        def get_bookmark_form_class(self):
            return MockForm

    return MockFormProvider()


@pytest.mark.parametrize(
    "bookmark_filter, expected_description",
    [
        ({}, ""),
        ({"case_reference": "GBSIEL/2023"}, "Case reference: GBSIEL/2023"),
        ({"case_officer": GOV_USER_ID}, "Licensing Unit case officer: John Smith"),
        ({"assigned_user": GOV_USER_ID}, "Case adviser: John Smith"),
        ({"status": "ogd_advice"}, "Case status: OGD Advice"),
        ({"control_list_entry": ["ML1", "ML1a"]}, "Control list entry: ML1, ML1a"),
        ({"submitted_from": "12-12-2010"}, "Submitted after: 12-12-2010"),
        ({"is_trigger_list": True}, "Trigger list: True"),
        ({"countries": ["DE"]}, "Country: Germany"),
        (
            {
                "regime_entry": [
                    "d73d0273-ef94-4951-9c51-c291eba949a0",  #  /PS-IGNORE
                    "c760976f-fd14-4356-9f23-f6eaf084475d",  #  /PS-IGNORE
                ],
            },
            "Regime entry: mtcr-1, wassenaar-1",
        ),
        (
            {
                "case_officer": GOV_USER_ID,
                "assigned_user": GOV_USER_ID,
                "status": "ogd_advice",
                "control_list_entry": ["ML1", "ML1a"],
                "submitted_from": "12-12-2010",
                "is_trigger_list": True,
                "countries": ["DE"],
            },
            "Case adviser: John Smith, Case status: OGD Advice, Control list entry: ML1, ML1a, Country: Germany, Licensing Unit case officer: John Smith, Submitted after: 12-12-2010, Trigger list: True",
        ),
        ({"invalid_field_name": "invalid field value"}, ""),
        (
            {
                "case_reference": "GBSIEL/2023",
                "invalid_field_name": "invalid field value",
            },
            "Case reference: GBSIEL/2023",
        ),
        (
            {
                "case_officer": "not-a-real-id",
            },
            "",
        ),
        (
            {
                "case_reference": "GBSIEL/2023",
                "case_officer": "not-a-real-id",
            },
            "Case reference: GBSIEL/2023",
        ),
    ],
)
def test_description_from_filter(
    request_with_session,
    bookmark_filter,
    expected_description,
    mock_form_provider,
):
    bookmarks = new_bookmarks(bookmark_filter)
    enricher = BookmarkEnricher(request_with_session, "/queues/", mock_form_provider)
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 1
    assert enriched[0]["description"] == expected_description


@pytest.mark.parametrize(
    "bookmark_filter, expected_description, expected_url_params",
    [
        (
            {"submitted_from": "07-06-2022"},
            "Submitted after: 07-06-2022",
            "submitted_from_0=7&submitted_from_1=6&submitted_from_2=2022",
        ),
        (
            {"submitted_to": "23-11-1990"},
            "Submitted before: 23-11-1990",
            "submitted_to_0=23&submitted_to_1=11&submitted_to_2=1990",
        ),
        (
            {"finalised_from": "31-12-2007"},
            "Finalised after: 31-12-2007",
            "finalised_from_0=31&finalised_from_1=12&finalised_from_2=2007",
        ),
        (
            {"finalised_to": "01-03-2011"},
            "Finalised before: 01-03-2011",
            "finalised_to_0=1&finalised_to_1=3&finalised_to_2=2011",
        ),
        (
            {"countries": ["DE"]},
            "Country: Germany",
            "countries=DE",
        ),
        (
            {
                "regime_entry": ["d73d0273-ef94-4951-9c51-c291eba949a0"],  #  /PS-IGNORE
            },
            "Regime entry: wassenaar-1",
            "regime_entry=d73d0273-ef94-4951-9c51-c291eba949a0",  #  /PS-IGNORE
        ),
        (
            {
                "regime_entry": [
                    "d73d0273-ef94-4951-9c51-c291eba949a0",  #  /PS-IGNORE
                    "c760976f-fd14-4356-9f23-f6eaf084475d",  #  /PS-IGNORE
                ],
            },
            "Regime entry: mtcr-1, wassenaar-1",
            "regime_entry=d73d0273-ef94-4951-9c51-c291eba949a0&regime_entry=c760976f-fd14-4356-9f23-f6eaf084475d",  #  /PS-IGNORE
        ),
        (
            {"control_list_entry": ["ML1", "ML1a"]},
            "Control list entry: ML1, ML1a",
            "control_list_entry=ML1&control_list_entry=ML1a",
        ),
        (
            {"flags": ["798d5e92-c31a-48cc-9e6b-d3fc6dfd65f2", "e50f5cd3-331c-4914-b618-ee6eb67a081c"]},
            "Flags: AG Review Required, BAE",
            "flags=798d5e92-c31a-48cc-9e6b-d3fc6dfd65f2&flags=e50f5cd3-331c-4914-b618-ee6eb67a081c",
        ),
        (
            {"is_trigger_list": True},
            "Trigger list: True",
            "is_trigger_list=True",
        ),
        (
            {"max_total_value": "200.0"},
            "Max total value (£): 200.0",
            "max_total_value=200.0",
        ),
    ],
)
def test_enrich_bookmark_for_display(
    request_with_session,
    bookmark_filter,
    expected_description,
    expected_url_params,
    mock_form_provider,
):
    bookmarks = new_bookmarks(bookmark_filter)

    enricher = BookmarkEnricher(request_with_session, "/queues/", mock_form_provider)
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 1
    assert enriched[0]["description"] == expected_description
    assert enriched[0]["url"] == f"/queues/?{expected_url_params}"


def test_enrich_bookmark_for_display_custom_base_url(
    request_with_session,
    mock_form_provider,
):
    bookmarks = new_bookmarks({"is_trigger_list": True})

    enricher = BookmarkEnricher(
        request_with_session,
        "/queues/abcd",
        mock_form_provider,
    )
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 1
    assert enriched[0]["description"] == "Trigger list: True"
    assert enriched[0]["url"] == f"/queues/abcd?is_trigger_list=True"


class ObjectToForceException:
    def __str__(self):
        raise Exception("This object breaks when str() called")


def test_enrich_bookmark_for_display_filters_out_errors(
    request_with_session,
    mock_form_provider,
):
    bookmark_filter = {"dodgy_filter_entry": ObjectToForceException()}
    bookmarks = new_bookmarks(bookmark_filter)

    enricher = BookmarkEnricher(request_with_session, "/queues/", mock_form_provider)
    enriched = enricher.enrich_for_display(bookmarks)

    assert len(enriched) == 0


@pytest.mark.parametrize(
    "name, filter_data, expected_filter_data",
    [
        (
            "Test unwanted entries are removed",
            {
                "case_reference": "ABC/123",
                "csrfmiddlewaretoken": "csrfmiddlewaretoken",
                "save": True,
                "save_filter": True,
                "saved_filter_description": "Filter_1",
                "saved_filter_name": "Name",
                "return_to": "/return-to/",
            },
            {"case_reference": "ABC/123"},
        ),
        (
            "Test removed falsey values",
            {
                "None": None,
                "False": False,
                "empty string": "",
            },
            {},
        ),
        (
            "Test decimal value converted properly",
            {"max_total_value": Decimal(200)},
            {"max_total_value": "200"},
        ),
        (
            "Test date value converted properly",
            {"a_date": datetime.date(2020, 10, 1)},
            {"a_date": "01-10-2020"},
        ),
    ],
)
def test_enrich_filter_for_saving(name, filter_data, expected_filter_data):
    actual_filter = enrich_filter_for_saving(filter_data)

    assert sorted(actual_filter.items()) == sorted(expected_filter_data.items())
