import os
import re
import pytest
import requests

from dotenv import load_dotenv

from django.conf import settings
from django.core.files.storage import Storage
from django.test import Client

from conf import exporter

from core import client


DEFAULT_ENVFILE = "exporter.env"


def pytest_configure(config):
    """
    Load exporter env variables automagically
    """
    if not os.environ.get("PIPENV_DOTENV_LOCATION"):
        load_dotenv(dotenv_path=DEFAULT_ENVFILE, override=True)

    # Force mock_sso django application to be activated for test environments;
    # must be activated up front for mock_sso django app urls to be added
    settings.MOCK_SSO_ACTIVATE_ENDPOINTS = True
    settings.MOCK_SSO_USER_EMAIL = "test@example.net"
    settings.MOCK_SSO_USER_FIRST_NAME = "test"
    settings.MOCK_SSO_USER_LAST_NAME = "user"


@pytest.fixture(autouse=True)
def upload_handler():
    settings.FILE_UPLOAD_HANDLERS = ["django.core.files.uploadhandler.MemoryFileUploadHandler"]


@pytest.fixture
def lite_api_user_id():
    return "d355428a-64cb-4347-853b-afcacee15d93"


@pytest.fixture
def request_with_session(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    return request


@pytest.fixture
def mock_exporter_user(requests_mock, lite_api_user_id):
    url = client._build_absolute_uri("/users/authenticate/")
    data = {
        "user": {
            "id": 123,
            "email": "foo@example.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "status": "Active",
            "token": "foo",
            "lite_api_user_id": lite_api_user_id,
        }
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_exporter_user_me(requests_mock, lite_api_user_id):
    url = client._build_absolute_uri("/users/me/")
    data = {
        "user": {
            "id": 123,
            "email": "foo@example.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "status": "Active",
            "token": "foo",
            "lite_api_user_id": lite_api_user_id,
        },
        "role": {
            "id": "00000000-0000-0000-0000-000000000001",
            "permissions": [
                "ADMINISTER_USERS",
                "ADMINISTER_SITES",
                "EXPORTER_ADMINISTER_ROLES",
                "SUBMIT_LICENCE_APPLICATION",
                "SUBMIT_CLEARANCE_APPLICATION",
            ],
        },
        "organisations": [
            {
                "id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",
                "name": "Archway Communications",
                "joined_at": "2020-06-29T09:30:58.425994Z",
                "status": {"key": "active", "value": "Active"},
            }
        ],
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def authorized_client_factory(client: Client, settings, organisation_pk):
    """
    returns a factory to make a authorized client for a mock_exporter_user,

    the factory only expects the value of "user" inside the object returned by
    the mock_exporter_user fixture
    """

    def _inner(user):
        session = client.session
        session["first_name"] = user["first_name"]
        session["last_name"] = user["last_name"]
        session["user_token"] = user["token"]
        session["lite_api_user_id"] = user["lite_api_user_id"]
        session["email"] = user["email"]
        session["organisation"] = organisation_pk
        session[settings.TOKEN_SESSION_KEY] = {
            "access_token": "mock_access_token",
            "expires_in": 36000,
            "token_type": "Bearer",
            "scope": ["read", "write"],
            "refresh_token": "mock_refresh_token",
        }
        session.save()
        client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
        return client

    yield _inner


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture()
def mock_get_profile(requests_mock, mock_exporter_user):
    url = exporter.AUTHBROKER_PROFILE_URL
    yield requests_mock.get(url=url, json={"sub": "123456789xyzqpr", "email": mock_exporter_user["user"]["email"]})


@pytest.fixture(autouse=True)
def mock_authenticate_user_save(requests_mock, mock_exporter_user):
    url = client._build_absolute_uri("/user/authenticate/")
    yield requests_mock.post(url=url)


@pytest.fixture
def mock_sites(requests_mock, mock_exporter_user, mock_exporter_user_me):
    organisation_id = mock_exporter_user_me["organisations"][0]["id"]
    url = client._build_absolute_uri(
        f"/organisations/{organisation_id}/sites/?exclude=&get_total_users=False&postcode="
    )
    data = {
        "sites": [
            {
                "id": "f733084d-5a11-4a41-a55b-974d2fb779a7",
                "name": "Site1",
                "address": {
                    "address": None,
                    "id": "3f611bdb-ee89-41b5-a6f0-26f8b1182016",
                    "address_line_1": "42 Question Road",
                    "address_line_2": "",
                    "city": "London",
                    "region": "London",
                    "postcode": "Islington",
                    "country": {
                        "id": "GB",
                        "name": "United Kingdom",
                        "type": "gov.uk Country",
                        "is_eu": True,
                    },
                },
            },
            {
                "id": "f345084d-9a22-4a41-a55b-974d2fb789a9",
                "name": "Site2",
                "address": {
                    "address": None,
                    "id": "5h611bdb-ee89-41b5-a6f0-26f8b1182019",
                    "address_line_1": "43 Question Road",
                    "address_line_2": "",
                    "city": "Birmingham",
                    "region": "Midlands",
                    "postcode": "B7TTTT",
                    "country": {
                        "id": "GB",
                        "name": "United Kingdom",
                        "type": "gov.uk Country",
                        "is_eu": True,
                    },
                },
            },
        ]
    }
    requests_mock.get(url=url, json=data)
    return data


@pytest.fixture
def mock_organisation_users_list(requests_mock, mock_exporter_user, mock_exporter_user_me):
    organisation_id = mock_exporter_user_me["organisations"][0]["id"]
    url = client._build_absolute_uri(f"/organisations/{organisation_id}/users/")
    data = {"results": []}
    requests_mock.get(url=url, json=data)
    return data


@pytest.fixture
def mock_countries(requests_mock):
    url = client._build_absolute_uri("/static/countries/")
    # in relity there are around 275 countries
    data = {
        "countries": [
            {"id": "AE-AZ", "name": "Abu Dhabi", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AF", "name": "Afghanistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-AJ", "name": "Ajman", "type": "gov.uk Territory", "is_eu": False},
            {"id": "IN", "name": "India", "type": "gov.uk Territory", "is_eu": False},
            {"id": "US", "name": "United States", "type": "gov.uk Territory", "is_eu": False},
        ]
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def mock_units(requests_mock):
    url = client._build_absolute_uri("/static/units/")
    data = {
        "units": {
            "GRM": "Gram",
            "KGM": "Kilogram",
            "NAR": "Items",
            "MTK": "Square metre",
            "MTR": "Metre",
            "LTR": "Litre",
            "MTQ": "Cubic metre",
        }
    }

    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_notifications(requests_mock):
    url = client._build_absolute_uri("/users/notifications/")
    data = {}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_has_existing_applications_and_licences_and_nlrs(requests_mock):
    url = client._build_absolute_uri("/applications/existing/")
    data = {"applications": True}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture()
def data_organisations():
    return [
        {"id": "9c2222db-98e5-47e8-9e01-653354e95311", "name": "org1"},
        {"id": "9c2222db-98e5-47e8-9e01-653354e95222", "name": "org2"},
    ]


@pytest.fixture
def mock_get_organisation(requests_mock, mock_exporter_user_me):
    organisation_id = mock_exporter_user_me["organisations"][0]["id"]
    organisation_name = mock_exporter_user_me["organisations"][0]["name"]
    url = client._build_absolute_uri(f"/organisations/{organisation_id}")
    data = {"id": organisation_id, "name": organisation_name}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture
def no_op_storage(mocker):
    class NoOpStorage(Storage):
        def save(self, name, content, max_length=None):
            return name

        def open(self, name, mode="rb"):
            return None

        def delete(self, name):
            pass

    mocker.patch("core.wizard.views.BaseSessionWizardView.file_storage", new=NoOpStorage())


@pytest.fixture
def good_id(data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    return good["id"]


@pytest.fixture
def complete_item_summary(good_id):
    return (
        (
            "is-firearm-product",
            "No",
            "Is it a firearm product?",
        ),
        (
            "product-category",
            "It's a complete product",
            "Select the product category",
        ),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "part-number",
            "44",
            "Part number",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "uses-information-security",
            "No",
            "Does the product include cryptography or other information security features?",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "product-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/product-list/{good_id}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


@pytest.fixture
def component_accessory_summary(good_id):
    return (
        (
            "is-firearm-product",
            "No",
            "Is it a firearm product?",
        ),
        (
            "product-category",
            "It forms part of a product",
            "Select the product category",
        ),
        (
            "is-material-substance",
            "No, it's a component, accessory or module",
            "Is it a material or substance?",
        ),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        ("is-component", "Yes", "Is the product a component?"),
        ("component-type", "Modified for hardware", "What type of component is it?"),
        ("modified-details", "modified details", "Provide details of the modifications and the specific hardware"),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "part-number",
            "44",
            "Part number",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "uses-information-security",
            "No",
            "Does the product include cryptography or other information security features?",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "product-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/product-list/{good_id}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


@pytest.fixture
def technology_summary(good_id):
    return (
        (
            "is-firearm-product",
            "No",
            "Is it a firearm product?",
        ),
        (
            "non-firearm-category",
            "It helps to operate a product",
            "Select the product category",
        ),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "part-number",
            "44",
            "Enter the part number",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "security-features",
            "Yes",
            "Does the product include cryptography or other information security features?",
        ),
        (
            "security-feature-details",
            "security features",
            "Provide details of the cryptography or information security features",
        ),
        (
            "declared-at-customs",
            "Yes",
            "Will the product be declared at customs?",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "product-document",
            f'<a class="govuk-link govuk-link--no-visited-state" href="/product-list/{good_id}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


@pytest.fixture
def get_units_mock(requests_mock):
    requests_mock.get(
        "/static/units/", json={"units": {"NAR": "Items", "TON": "Tonne(s)", "KGM": "Kilogram(s)", "GRM": "Gram(s)"}}
    )


@pytest.fixture(autouse=True)
def mock_case_activity_system_user(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/activity/")
    data = {"activity": []}
    requests_mock.get(url=url, json=data)
    yield data


@pytest.fixture(autouse=True)
def mock_ecju_queries(data_standard_case, data_ecju_queries, requests_mock):
    requests_mock.get(
        url=rf"/cases/{data_standard_case['case']['id']}/ecju-queries/",
        json=data_ecju_queries,
    )
    yield data_ecju_queries


@pytest.fixture
def mock_update_survey(requests_mock, survey_id):
    survey_url = client._build_absolute_uri(f"/survey/{survey_id}")
    return requests_mock.put(
        survey_url,
        json={"id": survey_id},
        status_code=200,
    )


@pytest.fixture
def mock_post_survey(requests_mock, survey_id):
    survey_url = client._build_absolute_uri(f"/survey/")
    return requests_mock.post(
        survey_url,
        json={"id": survey_id},
        status_code=201,
    )


@pytest.fixture
def mock_get_survey(requests_mock, survey_id):
    survey_url = client._build_absolute_uri(f"/survey/{survey_id}")
    return requests_mock.get(
        survey_url,
        json={"id": survey_id},
        status_code=200,
    )


@pytest.fixture
def mock_get_application(requests_mock, application_pk, application_reference_number):
    return requests_mock.get(
        client._build_absolute_uri(f"/applications/{application_pk}"),
        json={"id": application_pk, "reference_code": application_reference_number, "status": "submitted"},
        status_code=200,
    )
