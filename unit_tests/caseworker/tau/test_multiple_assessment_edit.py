import pytest
from bs4 import BeautifulSoup

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_regime_entries,
    mock_application_good_documents,
    mock_good_precedent_endpoint_empty,
    mock_mtcr_entries_get,
    mock_wassenaar_entries_get,
    mock_nsg_entries_get,
    mock_cwc_entries_get,
    mock_ag_entries_get,
):
    yield


@pytest.fixture
def edit_multiple_assessments_url(data_standard_case):
    return reverse(
        "cases:tau:multiple_edit",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


def assert_cle_select(soup, id_prefix, expected_choices):
    cle_select = soup.find("select", id=f"{id_prefix}control_list_entries")
    assert cle_select
    options = cle_select.select("option")
    options_choices = {"values": [], "selected": []}
    for option in options:
        options_choices["values"].append(option["value"])
        if option.has_attr("selected"):
            options_choices["selected"].append(option["value"])
    assert options_choices == expected_choices


def test_edit_multiple_assessments_GET(
    authorized_client,
    edit_multiple_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
):
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_1["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]
    good_on_application_2["control_list_entries"] = [{"rating": "ML1"}]

    response = authorized_client.get(edit_multiple_assessments_url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1", {"class": "govuk-heading-l"}).text == "Edit assessments"

    table = soup.find("table", id="tau-form")
    assert table
    table_rows = table.select("tbody tr")
    assert len(table_rows) == 2

    def get_td_text(table_row):
        return [td.text.strip().strip() for td in table_row.findAll("td", {"class": "govuk-table__cell"})]

    assert get_td_text(table_rows[0]) == [
        "1.",
        "p1 44",
        "ML1 ML1a",  # The text value of a multiselect is all of it's options - not selected options
        "",
        "wassenaar-1 mtcr-1 nsg-1",
        "",
        "",
        "test comment",
    ]
    assert get_td_text(table_rows[1]) == [
        "2.",
        "p2 44",
        "ML1 ML1a",  # The text value of a multiselect is all of it's options - not selected options
        "",
        "wassenaar-1 mtcr-1 nsg-1",
        "",
        "",
        "test assesment note",
    ]

    assert_cle_select(soup, "id_form-0-", {"values": ["ML1", "ML1a"], "selected": ["ML1", "ML1a"]})
    assert_cle_select(soup, "id_form-1-", {"values": ["ML1", "ML1a"], "selected": ["ML1"]})


@pytest.mark.parametrize(
    "querystring, expected_line_numbers",
    (
        ("?line_numbers=1&line_numbers=2", [1, 2]),
        ("?line_numbers=1", [1]),
        ("?line_numbers=1&line_numbers=foo", [1]),
        ("?line_numbers=1&line_numbers=8", [1]),
        ("", [1, 2]),
    ),
)
def test_edit_multiple_assessments_GET_selected_product(
    authorized_client,
    edit_multiple_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    querystring,
    expected_line_numbers,
):
    """
    Test multiple edit page where products to edit are selected via GET parameter.
    """
    response = authorized_client.get(edit_multiple_assessments_url + querystring)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="tau-form")
    assert table

    line_numbers = [
        int(td.text.strip().strip().replace(".", "")) for td in table.findAll("td", {"class": "line-number"})
    ]
    assert line_numbers == expected_line_numbers


def test_edit_multiple_assessments_POST_success(
    authorized_client,
    requests_mock,
    edit_multiple_assessments_url,
    tau_assessment_url,
    wassenaar_regime_entry,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 2,
        "form-INITIAL_FORMS": 2,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 2,
        "form-0-id": good_on_application_1["id"],
        "form-0-control_list_entries": ["ML1", "ML1a"],
        "form-0-licence_required": True,
        "form-0-report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
        "form-0-refer_to_ncsc": False,
        "form-0-comment": "some multiple edit comment",
        "form-1-id": good_on_application_2["id"],
        "form-1-control_list_entries": ["ML1"],
        "form-1-licence_required": True,
        "form-1-report_summary_prefix": good_on_application_2["report_summary_prefix"]["id"],
        "form-1-report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
        "form-1-refer_to_ncsc": True,
        "form-1-regimes": [wassenaar_regime_entry["pk"]],
        "form-1-comment": "some multiple edit comment",
    }

    response = authorized_client.post(edit_multiple_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert mocked_assessment_endpoint.last_request.json() == [
        {
            "control_list_entries": ["ML1", "ML1a"],
            "report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
            "report_summary_prefix": "",
            "comment": "some multiple edit comment",
            "id": good_on_application_1["id"],
            "is_good_controlled": True,
            "regime_entries": [],
            "is_ncsc_military_information_security": False,
        },
        {
            "control_list_entries": ["ML1"],
            "report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
            "report_summary_prefix": good_on_application_2["report_summary_prefix"]["id"],
            "comment": "some multiple edit comment",
            "id": good_on_application_2["id"],
            "is_good_controlled": True,
            "regime_entries": [wassenaar_regime_entry["pk"]],
            "is_ncsc_military_information_security": True,
        },
    ]
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = f"You have edited 2 product assessments on Case {data_standard_case['case']['reference_code']}"
    assert messages == [expected_message]
    assert response.redirect_chain[-1][0] == tau_assessment_url


def test_edit_multiple_assessments_POST_single_product_success(
    authorized_client,
    requests_mock,
    edit_multiple_assessments_url,
    tau_assessment_url,
    wassenaar_regime_entry,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})
    good_on_application = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good_on_application["id"],
        "form-0-control_list_entries": ["ML1", "ML1a"],
        "form-0-licence_required": True,
        "form-0-report_summary_subject": good_on_application["report_summary_subject"]["id"],
        "form-0-refer_to_ncsc": False,
        "form-0-comment": "some multiple edit comment",
    }

    response = authorized_client.post(edit_multiple_assessments_url, data, follow=True)
    assert response.status_code == 200
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = f"You have edited 1 product assessment on Case {data_standard_case['case']['reference_code']}"
    assert messages == [expected_message]
    assert response.redirect_chain[-1][0] == tau_assessment_url


def test_edit_multiple_assessments_POST_uncontrolled_with_cle(
    authorized_client,
    requests_mock,
    edit_multiple_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good_on_application_1["id"],
        "form-0-control_list_entries": ["ML1", "ML1a"],
        "form-0-licence_required": False,
        "form-0-report_summary_subject": good_on_application_2["report_summary_subject"]["id"],
        "form-0-refer_to_ncsc": False,
        "form-0-comment": "some multiple edit comment",
    }

    response = authorized_client.post(edit_multiple_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert not mocked_assessment_endpoint.called
    assert response.context["formset"].forms[0].errors == {
        "control_list_entries": ["Remove control list entries or select 'Licence required'"]
    }


def test_edit_multiple_assessments_POST_controlled_missing_required_values(
    authorized_client,
    requests_mock,
    edit_multiple_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    api_make_assessment_url,
):
    mocked_assessment_endpoint = requests_mock.put(api_make_assessment_url, json={})
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good_on_application_1["id"],
        "form-0-control_list_entries": [],
        "form-0-licence_required": True,
        "form-0-refer_to_ncsc": False,
        "form-0-comment": "some multiple edit comment",
    }

    response = authorized_client.post(edit_multiple_assessments_url, data, follow=True)
    assert response.status_code == 200
    assert not mocked_assessment_endpoint.called
    assert response.context["formset"][0].errors == {
        "control_list_entries": ["Enter a control list entry or unselect 'Licence required'"],
        "report_summary_subject": ["Enter a report summary or unselect 'Licence required'"],
    }
