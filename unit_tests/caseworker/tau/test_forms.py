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
                "goods": ["Select the products that you want to assess"],
                "does_not_have_control_list_entries": [
                    "Select a control list entry or select 'This product does not have a control list entry'"
                ],
            },
        ),
        # Valid form
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
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
                "comments": "test",
            },
            True,
            {},
        ),
        # Invalid good-id
        (
            {"goods": ["test-id-not"], "report_summary": "test", "does_not_have_control_list_entries": True},
            False,
            {"goods": ["Select a valid choice. test-id-not is not one of the available choices."]},
        ),
        # Missing goods
        (
            {"goods": [], "report_summary": "test", "does_not_have_control_list_entries": True},
            False,
            {"goods": ["Select the products that you want to assess"]},
        ),
        # Missing report-summart
        (
            {"goods": ["test-id"], "report_summary": None, "does_not_have_control_list_entries": True},
            True,
            {},
        ),
        # does_not_have_control_list_entries=False and missing control_list_entries
        (
            {"goods": ["test-id"], "report_summary": "test", "does_not_have_control_list_entries": False},
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
            },
            True,
            {},
        ),
        # Set is_wassenaar to False
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": False,
            },
            True,
            {},
        ),
        # Set is_wassenaar to False
        (
            {
                "goods": ["test-id"],
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": True,
            },
            True,
            {},
        ),
    ),
)
def test_tau_assessment_form(data, valid, errors, rf):
    form = forms.TAUAssessmentForm(
        request=rf.get("/"),
        goods={"test-id": {}},
        control_list_entries_choices=[("test-rating", "test-text")],
        queue_pk="queue_pk",
        application_pk="application_pk",
        is_user_rfd=False,
        organisation_documents={},
        data=data,
    )
    assert form.is_valid() == valid
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
                "platform": {
                    "good": {
                        "item_category": {
                            "key": ProductCategories.PRODUCT_CATEGORY_PLATFORM,
                        },
                    },
                },
            },
            [
                (
                    "platform",
                    {
                        "good_on_application": {
                            "good": {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_PLATFORM}}
                        },
                        "summary": (
                            ("platform-summary",),
                            ("platform-product-on-application-summary",),
                        ),
                    },
                ),
            ],
        ),
        (
            {
                "material": {
                    "good": {
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
                            "good": {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_MATERIAL}}
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
                "software": {
                    "good": {
                        "item_category": {
                            "key": ProductCategories.PRODUCT_CATEGORY_SOFTWARE,
                        },
                    },
                },
            },
            [
                (
                    "software",
                    {
                        "good_on_application": {
                            "good": {"item_category": {"key": ProductCategories.PRODUCT_CATEGORY_SOFTWARE}}
                        },
                        "summary": (
                            ("software-summary",),
                            ("software-product-on-application-summary",),
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
    mocker.patch("caseworker.tau.forms.firearm_summary", return_value=(("firearm-summary",),))
    mocker.patch(
        "caseworker.tau.forms.firearm_on_application_summary",
        return_value=(("firearm-on-application-summary",),),
    )

    mocker.patch("caseworker.tau.forms.platform_summary", return_value=(("platform-summary",),))
    mocker.patch(
        "caseworker.tau.forms.platform_product_on_application_summary",
        return_value=(("platform-product-on-application-summary",),),
    )

    mocker.patch("caseworker.tau.forms.material_summary", return_value=(("material-summary",),))
    mocker.patch(
        "caseworker.tau.forms.material_product_on_application_summary",
        return_value=(("material-product-on-application-summary",),),
    )

    mocker.patch("caseworker.tau.forms.software_summary", return_value=(("software-summary",),))
    mocker.patch(
        "caseworker.tau.forms.software_product_on_application_summary",
        return_value=(("software-product-on-application-summary",),),
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
        queue_pk=queue_pk,
        application_pk=application_pk,
        is_user_rfd=False,
        organisation_documents={},
    )
    assert form.fields["goods"].choices == choices


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        # Empty form
        ({}, False, ["does_not_have_control_list_entries"]),
        # Valid form
        ({"report_summary": "test", "does_not_have_control_list_entries": True}, True, []),
        # Valid form - with comments
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": True,
                "comments": "test",
            },
            True,
            [],
        ),
        # Missing report-summary is ok when no CLEs
        (
            {"report_summary": None, "does_not_have_control_list_entries": True},
            True,
            [],
        ),
        # Missing report-summary is not ok when there are CLEs
        (
            {"report_summary": None, "control_list_entries": ["test-rating"]},
            False,
            ["report_summary"],
        ),
        # does_not_have_control_list_entries=False and missing control_list_entries
        (
            {"report_summary": "test", "does_not_have_control_list_entries": False},
            False,
            ["does_not_have_control_list_entries"],
        ),
        # does_not_have_control_list_entries=False but with control_list_entries
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
            },
            True,
            [],
        ),
        # Set is_wassenaar to False
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": False,
            },
            True,
            [],
        ),
        # Set is_wassenaar to True
        (
            {
                "report_summary": "test",
                "does_not_have_control_list_entries": False,
                "control_list_entries": ["test-rating"],
                "is_wassenaar": True,
            },
            True,
            [],
        ),
    ),
)
def test_tau_edit_form(data, valid, errors):
    form = forms.TAUEditForm(control_list_entries_choices=[("test-rating", "test-text")], data=data)
    assert form.is_valid() == valid
    assert list(form.errors.keys()) == errors
