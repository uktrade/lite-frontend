import pytest
import requests

from caseworker.cases.services import get_case
from caseworker.tau.services import get_first_precedents, group_gonas_by_good, get_latest_precedents


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def get_request(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    return request


@pytest.mark.parametrize(
    "precedents, results",
    (
        # One precedent for each good on the case
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "6a7fc61f-698b-46b6-9876-6ac0fddfb1a2",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": ["test-good-on-application-id-1"],
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": ["test-good-on-application-id-2"],
            },
        ),
        # One precedent for a good and none for the other
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "some-random-good",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": ["test-good-on-application-id-1"],
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": [],
            },
        ),
        # 2 precedent for one good - we will only return the first one!
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": ["test-good-on-application-id-2"],
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": [],
            },
        ),
        # 2 precedent for one good - with different cles and so we will return both
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1b"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": [
                    "test-good-on-application-id-1",
                    "test-good-on-application-id-2",
                ],
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": [],
            },
        ),
        # 2 precedent for one good - with multiple but same cles
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a", "ML1"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a", "ML1"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": ["test-good-on-application-id-2"],
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": [],
            },
        ),
        # 2 precedent for one good - with multiple same cles but in different order
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a", "ML1"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1", "ML1a"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": ["test-good-on-application-id-2"],
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": [],
            },
        ),
        # 2 precedent for one good - with multiple different cles
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a", "ML1"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1b", "ML1"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": [
                    "test-good-on-application-id-1",
                    "test-good-on-application-id-2",
                ],
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": [],
            },
        ),
    ),
)
def test_first_precedents(
    precedents,
    results,
    get_request,
    data_standard_case,
    mock_control_list_entries,
):
    # Mock requests to precedents api
    case_id = data_standard_case["case"]["id"]
    case = get_case(get_request, case_id)
    all_precedents = group_gonas_by_good(precedents)
    precedents = get_first_precedents(case, all_precedents)
    for good in data_standard_case["case"]["data"]["goods"]:
        good_id = good["id"]
        assert [p["id"] for p in precedents[good_id]] == results[good_id]


@pytest.mark.parametrize(
    "precedents, expected_latest_precedents",
    (
        # One precedent for each good on the case
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "6a7fc61f-698b-46b6-9876-6ac0fddfb1a2",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": "test-good-on-application-id-1",
                "6daad1c3-cf97-4aad-b711-d5c9a9f4586e": "test-good-on-application-id-2",
            },
        ),
        # One precedent for a good and none for the other
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "some-random-good",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": "test-good-on-application-id-1",
            },
        ),
        # 2 precedent for one good - we will only return the latest one!
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": "test-good-on-application-id-1",
            },
        ),
        # 2 precedent for one good - with different cles - so we will return the latest
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1b"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": "test-good-on-application-id-1",
            },
        ),
        # 2 precedent for one good - with multiple but same cles - return the latest
        (
            [
                {
                    "id": "test-good-on-application-id-1",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a", "ML1"],
                    "submitted_at": "2021-06-21T11:27:36.145000Z",
                },
                {
                    "id": "test-good-on-application-id-2",
                    "good": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                    "control_list_entries": ["ML1a", "ML1"],
                    "submitted_at": "2021-06-20T11:27:36.145000Z",
                },
            ],
            {
                "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e": "test-good-on-application-id-1",
            },
        ),
    ),
)
def test_get_latest_precedents(
    precedents,
    expected_latest_precedents,
    get_request,
    data_standard_case,
    mock_control_list_entries,
):
    # Mock requests to precedents api
    case_id = data_standard_case["case"]["id"]
    case = get_case(get_request, case_id)
    all_precedents = group_gonas_by_good(precedents)
    precedents = get_latest_precedents(case, all_precedents)
    for good_id, expected_latest_precedent_id in expected_latest_precedents.items():
        assert precedents[good_id]["id"] == expected_latest_precedent_id
