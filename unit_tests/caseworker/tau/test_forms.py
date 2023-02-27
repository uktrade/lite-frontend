import pytest
import requests
import uuid
from urllib import parse

from core.constants import (
    FirearmsProductType,
    ProductCategories,
)

from caseworker.tau import forms

REPORT_SUMMARY_PREFIXES = "report_summary_prefixes"
REPORT_SUMMARY_SUBJECTS = "report_summary_subjects"

PREFIX_API_RESPONSE = [
    {"id": "a4bb3d4d-1f6b-46a3-83fa-97a952fdd2c4", "name": "launching vehicles for"},  # /PS-IGNORE
    {"id": "b0849a92-4611-4e5b-b076-03562b138fb5", "name": "components for"},  # /PS-IGNORE
    {"id": "1a50d1cf-d22d-46bd-bf30-5a60d131fcce", "name": "promoting the supply of components for"},  # /PS-IGNORE
    {"id": "1c2d9032-e565-4158-a054-0112e8fabe1c", "name": "countermeasure equipment for"},  # /PS-IGNORE
    {"id": "76c33f3f-1da8-4fde-b259-ada269b43d34", "name": "counter-countermeasure equipment for"},  # /PS-IGNORE
]

SUBJECT_API_RESPONSE = [
    {"id": "0f6fbc0f-ce20-4adb-9066-9a6547e5c372", "name": "NBC protective/defensive equipment"},  # /PS-IGNORE
    {"id": "97ebace4-0a4c-4ce3-ad46-cce85ea473e8", "name": "TV cameras and control equipment"},  # /PS-IGNORE
    {"id": "3f169d4d-ef33-4555-861e-3c8aaf0d1ae1", "name": "acoustic vibration test equipment"},  # /PS-IGNORE
    {"id": "b1dd5e3b-380a-4393-8ba2-7d95e20b7679", "name": "acoustic vibration test equipment 2"},  # /PS-IGNORE
]


def configure_mock_request(client, rf):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    return request


@pytest.fixture
def report_summary_requests_mock(requests_mock):
    requests_mock.get(
        "/static/report_summary/prefixes/?name=components",
        json={REPORT_SUMMARY_PREFIXES: [PREFIX_API_RESPONSE[0], PREFIX_API_RESPONSE[1]]},
    )
    requests_mock.get(
        "/static/report_summary/prefixes/?name=components+for",
        json={REPORT_SUMMARY_PREFIXES: [PREFIX_API_RESPONSE[1], PREFIX_API_RESPONSE[2]]},
    )
    requests_mock.get(
        "/static/report_summary/prefixes/?name=cou",
        json={REPORT_SUMMARY_PREFIXES: [PREFIX_API_RESPONSE[3], PREFIX_API_RESPONSE[4]]},
    )
    requests_mock.get("/static/report_summary/prefixes/?name=gnu", json={REPORT_SUMMARY_PREFIXES: []})

    resp = PREFIX_API_RESPONSE[0]
    name = parse.quote_plus(resp["name"])
    requests_mock.get(f"/static/report_summary/prefixes/?name={name}", json={REPORT_SUMMARY_PREFIXES: [resp]})

    requests_mock.get(
        "/static/report_summary/subjects/?name=co",
        json={REPORT_SUMMARY_SUBJECTS: [SUBJECT_API_RESPONSE[1], SUBJECT_API_RESPONSE[2]]},
    )
    requests_mock.get(
        "/static/report_summary/subjects/?name=cou",
        json={REPORT_SUMMARY_SUBJECTS: [SUBJECT_API_RESPONSE[1], SUBJECT_API_RESPONSE[2]]},
    )
    requests_mock.get(
        "/static/report_summary/subjects/?name=acoustic", json={REPORT_SUMMARY_SUBJECTS: [SUBJECT_API_RESPONSE[2]]}
    )
    requests_mock.get(
        "/static/report_summary/subjects/?name=acoustic+vibration+test+equipment",
        json={REPORT_SUMMARY_SUBJECTS: [SUBJECT_API_RESPONSE[2], SUBJECT_API_RESPONSE[3]]},
    )
    requests_mock.get(
        "/static/report_summary/subjects/?name=acoustic+vibration+test+equipment+2",
        json={REPORT_SUMMARY_SUBJECTS: [SUBJECT_API_RESPONSE[3]]},
    )
    requests_mock.get("/static/report_summary/subjects/?name=aardvark", json={REPORT_SUMMARY_SUBJECTS: []})

    resp = SUBJECT_API_RESPONSE[1]
    name = parse.quote_plus(resp["name"])
    requests_mock.get(f"/static/report_summary/subjects/?name={name}", json={REPORT_SUMMARY_SUBJECTS: [resp]})

    for prefix_response in PREFIX_API_RESPONSE:
        requests_mock.get(
            f"/static/report_summary/prefixes/{prefix_response['id']}/", json={"report_summary_prefix": prefix_response}
        )
    requests_mock.get(
        f"/static/report_summary/prefixes/madeupid/",
        status_code=404,
    )

    for subject_response in SUBJECT_API_RESPONSE:
        requests_mock.get(
            f"/static/report_summary/subjects/{subject_response['id']}/",
            json={"report_summary_subject": subject_response},
        )
    requests_mock.get(
        f"/static/report_summary/subjects/madeupid/",
        status_code=404,
    )

    return requests_mock


@pytest.mark.parametrize(
    "name, data, valid, errors",
    (
        (
            "Empty form",
            {},
            False,
            {
                "does_not_have_control_list_entries": [
                    "Select a control list entry or select 'This product does not have a control list entry'"
                ],
                "goods": ["Select the products that you want to assess"],
                "regimes": ["Add a regime, or select none"],
                "report_summary_subject": ["Enter a report summary subject"],
            },
        ),
        (
            "Valid form",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        (
            "Valid form - with comments",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
                "comments": "test",
            },
            True,
            {},
        ),
        (
            "Invalid good-id",
            {
                "goods": ["test-id-not"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            False,
            {"goods": ["Select a valid choice. test-id-not is not one of the available choices."]},
        ),
        (
            "Missing goods",
            {
                "goods": [],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            False,
            {"goods": ["Select the products that you want to assess"]},
        ),
        (
            "Missing report-summary-subject",
            {
                "goods": ["test-id"],
                "report_summary_subject": "",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            False,
            {"report_summary_subject": ["Enter a report summary subject"]},
        ),
        (
            "does_not_have_control_list_entries=False and missing control_list_entries",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "regimes": ["NONE"],
            },
            False,
            {
                "does_not_have_control_list_entries": [
                    "Select a control list entry or select 'This product does not have a control list entry'"
                ]
            },
        ),
        (
            "does_not_have_control_list_entries=False but with control_list_entries",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        (
            "Does not have control list entries selected, but entries provided",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            False,
            {"does_not_have_control_list_entries": ["This is mutually exclusive with control list entries"]},
        ),
        (
            "Regimes NONE selected as well as another regime",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE", "MTCR"],
            },
            False,
            {
                "regimes": ["Add a regime, or select none"],
            },
        ),
        (
            "Wassenaar regime selected but subsection missing",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            "Wassenaar regime selected but subsection empty",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
                "wassenaar_entries": [],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            "MTCR regime selected but entry missing",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["MTCR"],
            },
            False,
            {
                "mtcr_entries": ["Type an entry for the Missile Technology Control Regime"],
            },
        ),
        (
            "MTCR regime selected but entry empty",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["MTCR"],
                "mtcr_entries": [],
            },
            False,
            {
                "mtcr_entries": ["Type an entry for the Missile Technology Control Regime"],
            },
        ),
        (
            "NSG regime selected but entry missing",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NSG"],
            },
            False,
            {
                "nsg_entries": ["Type an entry for the Nuclear Suppliers Group Regime"],
            },
        ),
        (
            "NSG regime selected but entry empty",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NSG"],
                "nsg_entries": [],
            },
            False,
            {
                "nsg_entries": ["Type an entry for the Nuclear Suppliers Group Regime"],
            },
        ),
        (
            "CWC regime selected but subsection missing",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
        (
            "CWC regime selected but subsection empty",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
                "cwc_entries": [],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
        (
            "AG regime selected but subsection missing",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["AG"],
            },
            False,
            {"ag_entries": ["Select an Australia Group subsection"]},
        ),
        (
            "AG regime selected but subsection empty",
            {
                "goods": ["test-id"],
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["AG"],
                "ag_entries": [],
            },
            False,
            {"ag_entries": ["Select an Australia Group subsection"]},
        ),
    ),
)
def test_tau_assessment_form(name, data, valid, errors, rf, client, report_summary_requests_mock):
    request = configure_mock_request(client, rf)
    form = forms.TAUAssessmentForm(
        request=request,
        goods={"test-id": {}},
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-value")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-value")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-value")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-value")],
        ag_entries=[("test-ag-entry", "test-ag-entry-value")],
        queue_pk="queue_pk",
        application_pk="application_pk",
        is_user_rfd=False,
        organisation_documents={},
        data=data,
    )
    assert form.is_valid() == valid, f"Has errors {dict(form.errors)}"
    assert form.errors == errors


@pytest.mark.parametrize(
    "goods, choices",
    (
        (
            {
                "no-data-no-summary": {},
            },
            [("no-data-no-summary", {"good_on_application": {}, "summary": None})],
        ),
        (
            {
                "empty-good-no-summary": {
                    "good": {},
                },
            },
            [
                (
                    "empty-good-no-summary",
                    {
                        "good_on_application": {"good": {}},
                        "summary": None,
                    },
                ),
            ],
        ),
        (
            {
                "no-item-category-no-summary": {
                    "good": {
                        "name": "name",
                    },
                },
            },
            [
                (
                    "no-item-category-no-summary",
                    {
                        "good_on_application": {"good": {"name": "name"}},
                        "summary": None,
                    },
                ),
            ],
        ),
        (
            {
                "unknown-item-category-no-summary": {
                    "good": {
                        "item_category": {
                            "key": "unknown-item-category",
                        },
                    },
                },
            },
            [
                (
                    "unknown-item-category-no-summary",
                    {
                        "good_on_application": {"good": {"item_category": {"key": "unknown-item-category"}}},
                        "summary": None,
                    },
                ),
            ],
        ),
        (
            {
                "firearm": {
                    "firearm_details": {
                        "type": {
                            "key": FirearmsProductType.FIREARMS,
                        },
                    },
                    "good": {
                        "id": "12345",
                        "item_category": {
                            "key": ProductCategories.PRODUCT_CATEGORY_FIREARM,
                        },
                    },
                }
            },
            [
                (
                    "firearm",
                    {
                        "good_on_application": {
                            "firearm_details": {
                                "type": {
                                    "key": FirearmsProductType.FIREARMS,
                                }
                            },
                            "good": {
                                "id": "12345",
                                "item_category": {
                                    "key": ProductCategories.PRODUCT_CATEGORY_FIREARM,
                                },
                            },
                        },
                        "summary": (
                            ("firearm-summary",),
                            ("firearm-on-application-summary",),
                        ),
                    },
                ),
            ],
        ),
        (
            {
                "complete_item": {
                    "good": {
                        "id": "12345",
                        "item_category": {
                            "key": ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM,
                        },
                    },
                },
            },
            [
                (
                    "complete_item",
                    {
                        "good_on_application": {
                            "good": {
                                "id": "12345",
                                "item_category": {"key": ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM},
                            }
                        },
                        "summary": (
                            ("complete_item-summary",),
                            ("complete_item-product-on-application-summary",),
                        ),
                    },
                ),
            ],
        ),
        (
            {
                "material": {
                    "good": {
                        "id": "12345",
                        "item_category": {
                            "key": ProductCategories.PRODUCT_CATEGORY_MATERIAL,
                        },
                    },
                },
            },
            [
                (
                    "material",
                    {
                        "good_on_application": {
                            "good": {
                                "id": "12345",
                                "item_category": {"key": ProductCategories.PRODUCT_CATEGORY_MATERIAL},
                            }
                        },
                        "summary": (
                            ("material-summary",),
                            ("material-product-on-application-summary",),
                        ),
                    },
                ),
            ],
        ),
        (
            {
                "technology": {
                    "good": {
                        "id": "12345",
                        "item_category": {
                            "key": ProductCategories.PRODUCT_CATEGORY_SOFTWARE,
                        },
                    },
                },
            },
            [
                (
                    "technology",
                    {
                        "good_on_application": {
                            "good": {
                                "id": "12345",
                                "item_category": {"key": ProductCategories.PRODUCT_CATEGORY_SOFTWARE},
                            }
                        },
                        "summary": (
                            ("technology-summary",),
                            ("technology-product-on-application-summary",),
                        ),
                    },
                ),
            ],
        ),
        (
            {
                "component_accessory": {
                    "good": {
                        "id": "12345",
                        "item_category": {
                            "key": ProductCategories.PRODUCT_CATEGORY_COMPONENT_ACCESSORY,
                        },
                    },
                },
            },
            [
                (
                    "component_accessory",
                    {
                        "good_on_application": {
                            "good": {
                                "id": "12345",
                                "item_category": {"key": ProductCategories.PRODUCT_CATEGORY_COMPONENT_ACCESSORY},
                            }
                        },
                        "summary": (
                            ("component-accessory-summary",),
                            ("component-accessory-product-on-application-summary",),
                        ),
                    },
                ),
            ],
        ),
    ),
)
def test_tau_assessment_form_goods_choices(
    mocker,
    rf,
    client,
    goods,
    choices,
    requests_mock,
    report_summary_requests_mock,
):
    mocker.patch("caseworker.cases.helpers.summaries.firearm_summary", return_value=(("firearm-summary",),))
    mocker.patch(
        "caseworker.cases.helpers.summaries.firearm_on_application_summary",
        return_value=(("firearm-on-application-summary",),),
    )

    mocker.patch("caseworker.cases.helpers.summaries.complete_item_summary", return_value=(("complete_item-summary",),))
    mocker.patch(
        "caseworker.cases.helpers.summaries.complete_item_product_on_application_summary",
        return_value=(("complete_item-product-on-application-summary",),),
    )

    mocker.patch("caseworker.cases.helpers.summaries.material_summary", return_value=(("material-summary",),))
    mocker.patch(
        "caseworker.cases.helpers.summaries.material_product_on_application_summary",
        return_value=(("material-product-on-application-summary",),),
    )

    mocker.patch("caseworker.cases.helpers.summaries.technology_summary", return_value=(("technology-summary",),))
    mocker.patch(
        "caseworker.cases.helpers.summaries.technology_product_on_application_summary",
        return_value=(("technology-product-on-application-summary",),),
    )

    mocker.patch(
        "caseworker.cases.helpers.summaries.component_accessory_summary",
        return_value=(("component-accessory-summary",),),
    )
    mocker.patch(
        "caseworker.cases.helpers.summaries.component_accessory_product_on_application_summary",
        return_value=(("component-accessory-product-on-application-summary",),),
    )

    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    good_pk = "12345"

    requests_mock.get(
        f"/applications/{application_pk}/goods/{good_pk}/documents/",
        json={"documents": []},
    )

    request = configure_mock_request(client, rf)

    form = forms.TAUAssessmentForm(
        request=request,
        goods=goods,
        control_list_entries_choices=[],
        wassenaar_entries=[],
        mtcr_entries=[],
        nsg_entries=[],
        cwc_entries=[],
        ag_entries=[],
        queue_pk=queue_pk,
        application_pk=application_pk,
        is_user_rfd=False,
        organisation_documents={},
    )
    assert form.fields["goods"].choices == choices


def test_tau_assessment_form_goods_choices_summary_has_fields_removed(
    mocker,
    rf,
    client,
    requests_mock,
):
    mocker.patch(
        "caseworker.tau.summaries.get_good_on_application_summary",
        return_value=(
            ("keep-value", "keep_value"),
            ("name", "to_remove"),
            ("is-good-controlled", "to_remove"),
            ("control-list-entries", "to_remove"),
            ("no-product-document-explanation", "to_remove"),
            ("product-document", "to_remove"),
            ("product-document-description", "to_remove"),
        ),
    )

    queue_pk = uuid.uuid4()
    application_pk = uuid.uuid4()
    good_pk = "12345"

    requests_mock.get(
        f"/applications/{application_pk}/goods/{good_pk}/documents/",
        json={"documents": []},
    )

    request = configure_mock_request(client, rf)

    form = forms.TAUAssessmentForm(
        request=request,
        goods={
            "12345": {
                "good": {
                    "id": "12345",
                },
            },
        },
        control_list_entries_choices=[],
        wassenaar_entries=[],
        mtcr_entries=[],
        nsg_entries=[],
        cwc_entries=[],
        ag_entries=[],
        queue_pk=queue_pk,
        application_pk=application_pk,
        is_user_rfd=False,
        organisation_documents={},
    )
    assert form.fields["goods"].choices == [
        (
            "12345",
            {
                "good_on_application": {"good": {"id": "12345"}},
                "summary": (("keep-value", "keep_value"),),
            },
        )
    ]


@pytest.mark.parametrize(
    "name, data, valid, errors",
    (
        (
            "Empty form",
            {},
            False,
            {
                "does_not_have_control_list_entries": [
                    "Select a control list entry or select 'This product does not have a control list entry'"
                ],
                "regimes": ["Add a regime, or select none"],
                "report_summary_subject": ["Enter a report summary subject"],
            },
        ),
        (
            "Valid form",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        (
            "Valid form with comments",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
                "comments": "test",
            },
            True,
            {},
        ),
        (
            "Missing report-summary-subject",
            {
                "report_summary_prefix": "madeupid",
                "report_summary_subject": "",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            False,
            {
                "report_summary_prefix": ["Enter a valid report summary prefix"],
                "report_summary_subject": ["Enter a report summary subject"],
            },
        ),
        (
            "Has no control list entries checked but control list entries missing",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "regimes": ["NONE"],
            },
            False,
            {
                "does_not_have_control_list_entries": [
                    "Select a control list entry or select 'This product does not have a control list entry'"
                ]
            },
        ),
        (
            "Has no control list entries unchecked and control list entries present",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        (
            "Marked as not have CLEs but has CLEs",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": True,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            False,
            {"does_not_have_control_list_entries": ["This is mutually exclusive with control list entries"]},
        ),
        (
            "Regime NONE and another selected",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE", "MTCR"],
            },
            False,
            {
                "regimes": ["Add a regime, or select none"],
            },
        ),
        (
            "Wassenaar regime selected but subsection missing",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            "Wassenaar regime selected but subsection empty",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
                "wassenaar_entries": [],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            "MTCR regime selected but entry missing",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["MTCR"],
            },
            False,
            {
                "mtcr_entries": ["Type an entry for the Missile Technology Control Regime"],
            },
        ),
        (
            "MTCR regime selected but entry empty",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["MTCR"],
                "mtcr_entries": [],
            },
            False,
            {
                "mtcr_entries": ["Type an entry for the Missile Technology Control Regime"],
            },
        ),
        (
            "NSG regime selected but entry missing",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NSG"],
            },
            False,
            {
                "nsg_entries": ["Type an entry for the Nuclear Suppliers Group Regime"],
            },
        ),
        (
            "NSG regime selected but entry empty",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NSG"],
                "nsg_entries": [],
            },
            False,
            {
                "nsg_entries": ["Type an entry for the Nuclear Suppliers Group Regime"],
            },
        ),
        (
            "CWC regime selected but subsection missing",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
        (
            "CWC regime selected but subsection empty",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
                "cwc_entries": [],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
        (
            "AG regime selected but subsection missing",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["AG"],
            },
            False,
            {"ag_entries": ["Select an Australia Group subsection"]},
        ),
        (
            "AG regime selected but subsection empty",
            {
                "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["AG"],
                "ag_entries": [],
            },
            False,
            {"ag_entries": ["Select an Australia Group subsection"]},
        ),
    ),
)
def test_tau_edit_form(name, data, valid, errors, rf, client, report_summary_requests_mock):
    request = configure_mock_request(client, rf)
    form = forms.TAUEditForm(
        request=request,
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-text")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-text")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-text")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-text")],
        ag_entries=[("test-ag-entry", "test-ag-entry-text")],
        data=data,
    )
    assert form.is_valid() == valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "name, prefix, expected_prefix_id, expected_prefix_name",
    [
        ("No prefix", "", None, None),
        ("Blank prefix", None, None, None),
        (
            "Valid prefix",
            PREFIX_API_RESPONSE[0]["id"],
            PREFIX_API_RESPONSE[0]["id"],
            PREFIX_API_RESPONSE[0]["name"],
        ),
        (
            "Valid prefix with multiple matches",
            PREFIX_API_RESPONSE[1]["id"],
            PREFIX_API_RESPONSE[1]["id"],
            PREFIX_API_RESPONSE[1]["name"],
        ),
    ],
)
def test_report_summary_valid_prefix(
    name, prefix, expected_prefix_id, expected_prefix_name, report_summary_requests_mock, rf, client
):
    request = configure_mock_request(client, rf)
    data = {
        "goods": ["test-id"],
        "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
        "does_not_have_control_list_entries": True,
        "regimes": ["NONE"],
    }
    if prefix is not None:
        data["report_summary_prefix"] = prefix

    form = forms.TAUEditForm(
        request=request,
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-text")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-text")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-text")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-text")],
        ag_entries=[("test-ag-entry", "test-ag-entry-text")],
        data=data,
    )
    assert form.is_valid()
    assert not form.errors
    assert form.fields["report_summary_prefix"].widget.attrs.get("data-name") == expected_prefix_name


@pytest.mark.parametrize(
    "name, additional_data, expected_name",
    (
        ("Invalid ID", {"report_summary_prefix": "madeupid"}, ""),
        (
            "Invalid prefix entered, no previous selection",
            {"report_summary_prefix": "", "_report_summary_prefix": "no matching entry"},
            None,
        ),
        (
            "Invalid prefix entered with previous selection",
            {"report_summary_prefix": PREFIX_API_RESPONSE[1]["id"], "_report_summary_prefix": "no matching entry"},
            PREFIX_API_RESPONSE[1]["name"],
        ),
    ),
)
def test_report_summary_invalid_prefix(name, additional_data, expected_name, report_summary_requests_mock, rf, client):
    request = configure_mock_request(client, rf)
    data = {
        "goods": ["test-id"],
        "report_summary_subject": SUBJECT_API_RESPONSE[1]["id"],
        "does_not_have_control_list_entries": True,
        "regimes": ["NONE"],
    }
    data.update(additional_data)

    form = forms.TAUEditForm(
        request=request,
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-text")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-text")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-text")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-text")],
        ag_entries=[("test-ag-entry", "test-ag-entry-text")],
        data=data,
    )
    assert not form.is_valid()
    assert form.errors["report_summary_prefix"] == ["Enter a valid report summary prefix"]
    assert form.fields["report_summary_prefix"].widget.attrs.get("data-name") == expected_name


@pytest.mark.parametrize(
    "name, subject, expected_subject_id, expected_subject_name",
    [
        (
            "Single subject",
            SUBJECT_API_RESPONSE[3]["id"],
            SUBJECT_API_RESPONSE[3]["id"],
            SUBJECT_API_RESPONSE[3]["name"],
        ),
        (
            "Multiple matches for subject",
            SUBJECT_API_RESPONSE[2]["id"],
            SUBJECT_API_RESPONSE[2]["id"],
            SUBJECT_API_RESPONSE[2]["name"],
        ),
    ],
)
def test_report_summary_valid_subject(
    name, subject, expected_subject_id, expected_subject_name, report_summary_requests_mock, rf, client
):
    request = configure_mock_request(client, rf)
    data = {
        "goods": ["test-id"],
        "report_summary_prefix": "",
        "does_not_have_control_list_entries": True,
        "regimes": ["NONE"],
    }
    data["report_summary_subject"] = subject

    form = forms.TAUEditForm(
        request=request,
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-text")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-text")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-text")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-text")],
        ag_entries=[("test-ag-entry", "test-ag-entry-text")],
        data=data,
    )
    assert form.is_valid()
    assert not form.errors
    assert form.fields["report_summary_subject"].widget.attrs["data-name"] == expected_subject_name


@pytest.mark.parametrize(
    "name, additional_data, expected_name",
    (
        ("Invalid ID", {"report_summary_subject": "madeupid"}, ""),
        (
            "Invalid prefix entered, no previous selection",
            {"report_summary_subject": "", "_report_summary_subject": "no matching entry"},
            None,
        ),
        (
            "Invalid prefix entered with previous selection",
            {"report_summary_subject": SUBJECT_API_RESPONSE[1]["id"], "_report_summary_subject": "no matching entry"},
            SUBJECT_API_RESPONSE[1]["name"],
        ),
    ),
)
def test_report_summary_invalid_subject(name, additional_data, expected_name, report_summary_requests_mock, rf, client):
    request = configure_mock_request(client, rf)
    data = {
        "goods": ["test-id"],
        "report_summary_prefix": "",
        "does_not_have_control_list_entries": True,
        "regimes": ["NONE"],
    }
    data.update(additional_data)

    form = forms.TAUEditForm(
        request=request,
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-text")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-text")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-text")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-text")],
        ag_entries=[("test-ag-entry", "test-ag-entry-text")],
        data=data,
    )
    assert not form.is_valid()
    assert "Enter a valid report summary subject" in form.errors["report_summary_subject"]
    assert form.fields["report_summary_subject"].widget.attrs.get("data-name") == expected_name
