import pytest
import requests
import uuid

from core.constants import (
    FirearmsProductType,
    ProductCategories,
)

from caseworker.tau import forms


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        # Empty form
        (
            {},
            False,
            {
                "does_not_have_control_list_entries": [
                    "Select a control list entry or select 'This product does not have a control list entry'"
                ],
                "goods": ["Select the products that you want to assess"],
                "regimes": ["Add a regime, or select none"],
            },
        ),
        # Valid form
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        # Valid form - with comments
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
                "comments": "test",
            },
            True,
            {},
        ),
        # Invalid good-id
        (
            {
                "goods": ["test-id-not"],
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            False,
            {"goods": ["Select a valid choice. test-id-not is not one of the available choices."]},
        ),
        # Missing goods
        (
            {
                "goods": [],
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            False,
            {"goods": ["Select the products that you want to assess"]},
        ),
        # Missing report-summary
        (
            {
                "goods": ["test-id"],
                "report_summary": None,
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        # does_not_have_control_list_entries=False and missing control_list_entries
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
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
        # does_not_have_control_list_entries=False but with control_list_entries
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            False,
            {"does_not_have_control_list_entries": ["This is mutually exclusive with control list entries"]},
        ),
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
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
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
                "wassenaar_entries": [],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
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
            {
                "goods": ["test-id"],
                "report_summary": "test",
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
            {
                "goods": ["test-id"],
                "report_summary": "test",
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
            {
                "goods": ["test-id"],
                "report_summary": "test",
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
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
                "cwc_entries": [],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
    ),
)
def test_tau_assessment_form(data, valid, errors, rf):
    form = forms.TAUAssessmentForm(
        request=rf.get("/"),
        goods={"test-id": {}},
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-value")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-value")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-value")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-value")],
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

    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    form = forms.TAUAssessmentForm(
        request=request,
        goods=goods,
        control_list_entries_choices=[],
        wassenaar_entries=[],
        mtcr_entries=[],
        nsg_entries=[],
        cwc_entries=[],
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

    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

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
    "data, valid, errors",
    (
        # Empty form
        (
            {},
            False,
            {
                "does_not_have_control_list_entries": [
                    "Select a control list entry or select 'This product does not have a control list entry'"
                ],
                "regimes": ["Add a regime, or select none"],
            },
        ),
        # Valid form
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        # Valid form - with comments
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
                "comments": "test",
            },
            True,
            {},
        ),
        # Missing report-summary
        (
            {
                "report_summary": None,
                "does_not_have_control_list_entries": True,
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        # does_not_have_control_list_entries=False and missing control_list_entries
        (
            {
                "report_summary": "test",
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
        # does_not_have_control_list_entries=False but with control_list_entries
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            True,
            {},
        ),
        # Marked as not have CLEs but has CLEs
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "control_list_entries": ["test-rating"],
                "regimes": ["NONE"],
            },
            False,
            {"does_not_have_control_list_entries": ["This is mutually exclusive with control list entries"]},
        ),
        (
            {
                "report_summary": "test",
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
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["WASSENAAR"],
                "wassenaar_entries": [],
            },
            False,
            {"wassenaar_entries": ["Select a Wassenaar Arrangement subsection"]},
        ),
        (
            {
                "report_summary": "test",
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
            {
                "report_summary": "test",
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
            {
                "report_summary": "test",
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
            {
                "report_summary": "test",
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
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "regimes": ["CWC"],
                "cwc_entries": [],
            },
            False,
            {"cwc_entries": ["Select a Chemical Weapons Convention subsection"]},
        ),
    ),
)
def test_tau_edit_form(data, valid, errors):
    form = forms.TAUEditForm(
        control_list_entries_choices=[("test-rating", "test-text")],
        wassenaar_entries=[("test-wassenaar-entry", "test-wassenaar-entry-text")],
        mtcr_entries=[("test-mtcr-entry", "test-mtcr-entry-text")],
        nsg_entries=[("test-nsg-entry", "test-nsg-entry-text")],
        cwc_entries=[("test-cwc-entry", "test-cwc-entry-text")],
        data=data,
    )
    assert form.is_valid() == valid
    assert form.errors == errors
