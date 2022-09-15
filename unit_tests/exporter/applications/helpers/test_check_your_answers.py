import pytest

from core.constants import CaseStatusEnum
from exporter.applications.helpers import check_your_answers


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


def test_convert_goods_on_application_no_answers(application, data_good_on_application):
    # given the canonical good does not have is_good_controlled set
    data_good_on_application["is_good_controlled"] = None
    data_good_on_application["good"]["is_good_controlled"] = None
    data_good_on_application["good"]["control_list_entries"] = []
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then the differences in export characteristics are highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'


def test_convert_goods_on_application_application_level_control_list_entries(application, data_good_on_application):
    data_good_on_application["good"]["control_list_entries"] = []

    # given the canonical good and good in application have different export control characteristics
    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then the differences in export characteristics are highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'


def test_convert_goods_on_application_application_level_control_list_entries_same(
    application, data_good_on_application
):
    # given the canonical good and good in application have same export control characteristics
    data_good_on_application["good"]["is_good_controlled"] = data_good_on_application["is_good_controlled"]
    data_good_on_application["good"]["control_list_entries"] = data_good_on_application["control_list_entries"]

    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then no difference is highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == (
        "<span data-definition-title='ML1' data-definition-text='Smooth-bore weapons...'>ML1</span>, "
        "<span data-definition-title='ML2' data-definition-text='Smooth-bore weapons...'>ML2</span>"
    )


def test_convert_goods_on_application_good_level_control_list_entries(application, data_good_on_application):
    # given the good has not been reviewed at application levcle
    data_good_on_application["is_good_controlled"] = None
    data_good_on_application["good"]["control_list_entries"] = []

    # when the shape is generated
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])

    # then no difference is highlighted
    assert len(actual) == 1
    assert actual[0]["Control list entries"] == '<span class="govuk-hint govuk-!-margin-0">N/A</span>'


def test_add_serial_numbers_link(application, data_good_on_application):
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    assert "firearm_details" not in data_good_on_application
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = None
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = {
        "serial_numbers_available": "NOT_AVAILABLE",
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = {
        "number_of_items": 3,
        "serial_numbers_available": "AVAILABLE",
        "serial_numbers": [],
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]

    data_good_on_application["firearm_details"] = {
        "number_of_items": 3,
        "serial_numbers_available": "AVAILABLE",
        "serial_numbers": [],
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application], is_summary=True)
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    data_good_on_application["firearm_details"] = {
        "number_of_items": 3,
        "serial_numbers_available": "AVAILABLE",
        "serial_numbers": ["111", "222", "333"],
    }
    actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]

    allowed_case_statuses = [CaseStatusEnum.SUBMITTED, CaseStatusEnum.FINALISED]
    for case_status in allowed_case_statuses:
        application["status"]["key"] = case_status
        data_good_on_application["firearm_details"] = {
            "number_of_items": 3,
            "serial_numbers_available": "AVAILABLE",
            "serial_numbers": [],
        }
        actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
        assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]

    disallowed_case_statuses = set(CaseStatusEnum.all()) - set(allowed_case_statuses)
    for case_status in disallowed_case_statuses:
        application["status"]["key"] = case_status
        data_good_on_application["firearm_details"] = {
            "number_of_items": 3,
            "serial_numbers_available": "AVAILABLE",
            "serial_numbers": [],
        }
        actual = check_your_answers.convert_goods_on_application(application, [data_good_on_application])
        assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]


def test_actions_column_is_balanced_across_rows(application, data_good_on_application):
    with_serial_numbers = {
        **data_good_on_application,
        **{
            "firearm_details": {
                "number_of_items": 3,
                "serial_numbers_available": "AVAILABLE",
                "serial_numbers": ["111", "222", "333"],
            }
        },
    }
    later_serial_numbers = {
        **data_good_on_application,
        **{
            "firearm_details": {
                "number_of_items": 3,
                "serial_numbers_available": "LATER",
                "serial_numbers": [],
            }
        },
    }

    actual = check_your_answers.convert_goods_on_application(application, [with_serial_numbers, with_serial_numbers])
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[0]
    assert '<span class="govuk-visually-hidden">Actions</a>' not in actual[1]

    actual = check_your_answers.convert_goods_on_application(application, [later_serial_numbers, later_serial_numbers])
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[1]

    actual = check_your_answers.convert_goods_on_application(application, [with_serial_numbers, later_serial_numbers])
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[0]
    assert '<span class="govuk-visually-hidden">Actions</a>' in actual[1]
