import pytest

from decimal import Decimal

from core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
    SerialChoices,
)
from core.summaries.reducers import (
    firearm_on_application_reducer,
    firearm_reducer,
    firearms_act_reducer,
    firearms_act_section1_reducer,
    firearms_act_section2_reducer,
    firearms_act_section5_reducer,
    has_product_document_reducer,
    is_deactivated_reducer,
    is_good_controlled_reducer,
    is_onward_exported_reducer,
    is_pv_graded_reducer,
    is_replica_reducer,
    serial_numbers_reducer,
    year_of_manufacture_reducer,
)


@pytest.mark.parametrize(
    "is_user_rfd",
    (
        True,
        False,
    ),
)
def test_firearm_reducer(is_user_rfd, mocker):
    mock_is_good_controlled_reducer = mocker.patch(
        "core.summaries.reducers.is_good_controlled_reducer", return_value=()
    )
    mock_is_pv_graded_reducer = mocker.patch("core.summaries.reducers.is_pv_graded_reducer", return_value=())
    mock_is_replica_reducer = mocker.patch("core.summaries.reducers.is_replica_reducer", return_value=())
    mock_firearms_act_reducer = mocker.patch("core.summaries.reducers.firearms_act_reducer", return_value=())
    mock_has_product_document_reducer = mocker.patch(
        "core.summaries.reducers.has_product_document_reducer", return_value=()
    )

    firearm_details = {
        "type": "firearm-details-type",
        "category": "firearm-details-category",
        "calibre": "firearm-details-calibre",
        "is-registered-firearms-dealer": is_user_rfd,
    }
    good = {
        "name": "good-name",
        "firearm_details": firearm_details,
    }
    organisation_documents = []
    assert firearm_reducer(good, is_user_rfd, organisation_documents) == (
        ("firearm-type", "firearm-details-type"),
        ("firearm-category", "firearm-details-category"),
        ("name", "good-name"),
        ("calibre", "firearm-details-calibre"),
        ("is-registered-firearms-dealer", is_user_rfd),
    )

    mock_is_good_controlled_reducer.assert_called_with(good)
    mock_is_pv_graded_reducer.assert_called_with(good)
    mock_is_replica_reducer.assert_called_with(firearm_details)
    mock_firearms_act_reducer.assert_called_with(firearm_details, is_user_rfd, organisation_documents)
    mock_has_product_document_reducer.assert_called_with(good)


@pytest.mark.parametrize(
    "good,output",
    (
        (
            {
                "is_good_controlled": {"key": "True"},
                "control_list_entries": ["ML1", "ML1a"],
            },
            (
                ("is-good-controlled", {"key": "True"}),
                (
                    "control-list-entries",
                    ["ML1", "ML1a"],
                ),
            ),
        ),
        (
            {
                "is_good_controlled": {"key": "False"},
                "control_list_entries": ["ML1", "ML1a"],
            },
            (("is-good-controlled", {"key": "False"}),),
        ),
    ),
)
def test_is_good_controlled_reducer(good, output):
    assert is_good_controlled_reducer(good) == output


@pytest.mark.parametrize(
    "good,output",
    (
        (
            {
                "is_pv_graded": {"key": "yes"},
                "pv_grading_details": {
                    "prefix": None,
                    "suffix": None,
                    "grading": "pv-grading-grading",
                    "issuing_authority": "pv-grading-issuing-authority",
                    "reference": "pv-grading-reference",
                    "date_of_issue": "pv-grading-date-of-issue",
                },
            },
            (
                ("is-pv-graded", "yes"),
                ("pv-grading-grading", "pv-grading-grading"),
                ("pv-grading-issuing-authority", "pv-grading-issuing-authority"),
                ("pv-grading-details-reference", "pv-grading-reference"),
                ("pv-grading-details-date-of-issue", "pv-grading-date-of-issue"),
            ),
        ),
        (
            {
                "is_pv_graded": "yes",
                "pv_grading_details": {
                    "prefix": None,
                    "suffix": None,
                    "grading": "pv-grading-grading",
                    "issuing_authority": "pv-grading-issuing-authority",
                    "reference": "pv-grading-reference",
                    "date_of_issue": "pv-grading-date-of-issue",
                },
            },
            (
                ("is-pv-graded", "yes"),
                ("pv-grading-grading", "pv-grading-grading"),
                ("pv-grading-issuing-authority", "pv-grading-issuing-authority"),
                ("pv-grading-details-reference", "pv-grading-reference"),
                ("pv-grading-details-date-of-issue", "pv-grading-date-of-issue"),
            ),
        ),
        (
            {
                "is_pv_graded": {"key": "yes"},
                "pv_grading_details": {
                    "prefix": "pv-grading-prefix",
                    "suffix": "pv-grading-suffix",
                    "grading": "pv-grading-grading",
                    "issuing_authority": "pv-grading-issuing-authority",
                    "reference": "pv-grading-reference",
                    "date_of_issue": "pv-grading-date-of-issue",
                },
            },
            (
                ("is-pv-graded", "yes"),
                ("pv-grading-prefix", "pv-grading-prefix"),
                ("pv-grading-grading", "pv-grading-grading"),
                ("pv-grading-suffix", "pv-grading-suffix"),
                ("pv-grading-issuing-authority", "pv-grading-issuing-authority"),
                ("pv-grading-details-reference", "pv-grading-reference"),
                ("pv-grading-details-date-of-issue", "pv-grading-date-of-issue"),
            ),
        ),
        (
            {
                "is_pv_graded": "yes",
                "pv_grading_details": {
                    "prefix": "pv-grading-prefix",
                    "suffix": "pv-grading-suffix",
                    "grading": "pv-grading-grading",
                    "issuing_authority": "pv-grading-issuing-authority",
                    "reference": "pv-grading-reference",
                    "date_of_issue": "pv-grading-date-of-issue",
                },
            },
            (
                ("is-pv-graded", "yes"),
                ("pv-grading-prefix", "pv-grading-prefix"),
                ("pv-grading-grading", "pv-grading-grading"),
                ("pv-grading-suffix", "pv-grading-suffix"),
                ("pv-grading-issuing-authority", "pv-grading-issuing-authority"),
                ("pv-grading-details-reference", "pv-grading-reference"),
                ("pv-grading-details-date-of-issue", "pv-grading-date-of-issue"),
            ),
        ),
        (
            {
                "is_pv_graded": {"key": "no"},
            },
            (("is-pv-graded", "no"),),
        ),
        (
            {
                "is_pv_graded": "no",
            },
            (("is-pv-graded", "no"),),
        ),
    ),
)
def test_is_pv_graded_reducer(good, output):
    assert is_pv_graded_reducer(good) == output


@pytest.mark.parametrize(
    "good,output",
    (
        (
            {
                "is_replica": True,
                "replica_description": "replica-description",
            },
            (
                ("is-replica", True),
                ("is-replica-description", "replica-description"),
            ),
        ),
        (
            {
                "is_replica": False,
            },
            (("is-replica", False),),
        ),
    ),
)
def test_is_replica_reducer(good, output):
    assert is_replica_reducer(good) == output


@pytest.mark.parametrize(
    "firearm_details,organisation_documents,output",
    (
        (
            {
                "firearms_act_section": "firearms_act_section5",
                "section_certificate_missing": True,
                "section_certificate_missing_reason": "missing-certificate-reason",
            },
            {},
            (
                ("section-5-certificate-missing", True),
                ("section-5-certificate-missing-reason", "missing-certificate-reason"),
            ),
        ),
        (
            {
                "firearms_act_section": "firearms_act_section5",
                "section_certificate_missing": False,
                "section_certificate_number": "section-certificate-number",
                "section_certificate_date_of_expiry": "2030-10-09",
            },
            {
                "section-five-certificate": "document",
            },
            (
                ("section-5-certificate-document", "document"),
                ("section-5-certificate-reference-number", "section-certificate-number"),
                ("section-5-certificate-date-of-expiry", "2030-10-09"),
            ),
        ),
    ),
)
def test_firearms_act_section5_reducer(firearm_details, organisation_documents, output):
    assert firearms_act_section5_reducer(firearm_details, organisation_documents) == output


@pytest.mark.parametrize(
    "firearm_details,is_user_rfd,organisation_documents,assert_firearms_act_section5_reducer_called,output",
    (
        (
            {
                "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            },
            True,
            [
                "document",
            ],
            True,
            (("is-covered-by-firearm-act-section-five", "Yes"),),
        ),
        (
            {
                "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
                "firearms_act_section": "firearms_act_section1",
            },
            False,
            [
                "document",
            ],
            True,
            (("firearms-act-1968-section", "firearms_act_section1"),),
        ),
        (
            {
                "is_covered_by_firearm_act_section_one_two_or_five": "No",
                "is_covered_by_firearm_act_section_one_two_or_five_explanation": "explanation",
            },
            False,
            ["document"],
            False,
            (("is-covered-by-firearm-act-section-one-two-or-five-explanation", "explanation"),),
        ),
        (
            {
                "is_covered_by_firearm_act_section_one_two_or_five": "No",
                "is_covered_by_firearm_act_section_one_two_or_five_explanation": None,
            },
            False,
            ["document"],
            False,
            (),
        ),
    ),
)
def test_firearms_act_reducer(
    mocker, firearm_details, is_user_rfd, organisation_documents, assert_firearms_act_section5_reducer_called, output
):
    mock_firearms_act_section5_reducer = mocker.patch(
        "core.summaries.reducers.firearms_act_section5_reducer", return_value=()
    )

    assert firearms_act_reducer(firearm_details, is_user_rfd, organisation_documents) == output
    if assert_firearms_act_section5_reducer_called:
        mock_firearms_act_section5_reducer.called_with(firearm_details, organisation_documents)


@pytest.mark.parametrize(
    "good,output",
    (
        (
            {
                "is_document_available": True,
                "is_document_sensitive": False,
                "documents": [
                    {
                        "description": "Product document description",
                    },
                ],
            },
            (
                ("has-product-document", True),
                ("is-document-sensitive", False),
                ("product-document", {"description": "Product document description"}),
                ("product-document-description", "Product document description"),
            ),
        ),
        (
            {
                "is_document_available": True,
                "is_document_sensitive": True,
            },
            (
                ("has-product-document", True),
                ("is-document-sensitive", True),
            ),
        ),
        (
            {
                "is_document_available": False,
                "no_document_comments": "No document comments",
            },
            (
                ("has-product-document", False),
                ("no-product-document-explanation", "No document comments"),
            ),
        ),
    ),
)
def test_has_product_document_reducer(good, output):
    assert has_product_document_reducer(good) == output


def test_firearm_on_application_reducer(mocker):
    mock_firearms_act_section1_reducer = mocker.patch(
        "core.summaries.reducers.firearms_act_section1_reducer",
        return_value=(),
    )
    mock_firearms_act_section2_reducer = mocker.patch(
        "core.summaries.reducers.firearms_act_section2_reducer",
        return_value=(),
    )
    mock_year_of_manufacture_reducer = mocker.patch(
        "core.summaries.reducers.year_of_manufacture_reducer",
        return_value=(),
    )
    mock_is_onward_exported_reducer = mocker.patch(
        "core.summaries.reducers.is_onward_exported_reducer",
        return_value=(),
    )
    mock_is_deactivated_reducer = mocker.patch(
        "core.summaries.reducers.is_deactivated_reducer",
        return_value=(),
    )
    mock_serial_numbers_reducer = mocker.patch(
        "core.summaries.reducers.serial_numbers_reducer",
        return_value=(),
    )

    good_on_application = {
        "firearm_details": {
            "number_of_items": 2,
        },
        "value": "14.44",
    }
    good_on_application_documents = {
        FirearmsActDocumentType.SECTION_1: {
            "id": "firearm-certificate-id",
        },
    }

    assert firearm_on_application_reducer(good_on_application, good_on_application_documents) == (
        ("number-of-items", 2),
        ("total-value", Decimal("14.44")),
    )
    mock_firearms_act_section1_reducer.assert_called_with(
        good_on_application["firearm_details"],
        good_on_application_documents,
    )
    mock_firearms_act_section2_reducer.assert_called_with(
        good_on_application["firearm_details"],
        good_on_application_documents,
    )
    mock_year_of_manufacture_reducer.assert_called_with(
        good_on_application["firearm_details"],
    )
    mock_is_onward_exported_reducer.assert_called_with(
        good_on_application["firearm_details"],
    )
    mock_is_deactivated_reducer.assert_called_with(
        good_on_application["firearm_details"],
    )
    mock_serial_numbers_reducer.assert_called_with(
        good_on_application["firearm_details"],
    )


@pytest.mark.parametrize(
    "firearm_details,good_on_application_documents,output",
    (
        (
            {},
            {},
            (),
        ),
        (
            {
                "firearms_act_section": "not-section-1",
            },
            {},
            (),
        ),
        (
            {
                "firearms_act_section": FirearmsActSections.SECTION_1,
                "section_certificate_missing": True,
                "section_certificate_missing_reason": "I do not have a firearm certificate",
            },
            {},
            (
                ("firearm-certificate-missing", True),
                ("firearm-certificate-missing-reason", "I do not have a firearm certificate"),
            ),
        ),
        (
            {
                "firearms_act_section": FirearmsActSections.SECTION_1,
                "section_certificate_missing": False,
                "section_certificate_date_of_expiry": "2024-02-01",
                "section_certificate_number": "12345",
            },
            {
                FirearmsActDocumentType.SECTION_1: {
                    "id": "firearm-certificate-id",
                },
            },
            (
                ("firearm-certificate", {"id": "firearm-certificate-id"}),
                ("firearm-certificate-expiry-date", "2024-02-01"),
                ("firearm-certificate-number", "12345"),
            ),
        ),
    ),
)
def test_firearms_act_section1_reducer(firearm_details, good_on_application_documents, output):
    assert firearms_act_section1_reducer(firearm_details, good_on_application_documents) == output


@pytest.mark.parametrize(
    "firearm_details,good_on_application_documents,output",
    (
        (
            {},
            {},
            (),
        ),
        (
            {
                "firearms_act_section": "not-section-2",
            },
            {},
            (),
        ),
        (
            {
                "firearms_act_section": FirearmsActSections.SECTION_2,
                "section_certificate_missing": True,
                "section_certificate_missing_reason": "I do not have a shotgun certificate",
            },
            {},
            (
                ("shotgun-certificate-missing", True),
                ("shotgun-certificate-missing-reason", "I do not have a shotgun certificate"),
            ),
        ),
        (
            {
                "firearms_act_section": FirearmsActSections.SECTION_2,
                "section_certificate_missing": False,
                "section_certificate_date_of_expiry": "2024-02-01",
                "section_certificate_number": "12345",
            },
            {
                FirearmsActDocumentType.SECTION_2: {
                    "id": "shotgun-certificate-id",
                },
            },
            (
                ("shotgun-certificate", {"id": "shotgun-certificate-id"}),
                ("shotgun-certificate-expiry-date", "2024-02-01"),
                ("shotgun-certificate-number", "12345"),
            ),
        ),
    ),
)
def test_firearms_act_section2_reducer(firearm_details, good_on_application_documents, output):
    assert firearms_act_section2_reducer(firearm_details, good_on_application_documents) == output


@pytest.mark.parametrize(
    "firearm_details,output",
    (
        (
            {
                "is_made_before_1938": None,
                "year_of_manufacture": 1980,
            },
            (("manufacture-year", 1980),),
        ),
        (
            {
                "is_made_before_1938": False,
            },
            (("made-before-1938", False),),
        ),
        (
            {"is_made_before_1938": True, "year_of_manufacture": 1930},
            (
                ("made-before-1938", True),
                ("manufacture-year", 1930),
            ),
        ),
        (
            {
                "category": {
                    "key": "RIFLE_MADE_BEFORE_1938",
                },
                "year_of_manufacture": 1930,
            },
            (("manufacture-year", 1930),),
        ),
        (
            {
                "category": {
                    "key": "COMBINATION_GUN_MADE_BEFORE_1938",
                },
                "year_of_manufacture": 1930,
            },
            (("manufacture-year", 1930),),
        ),
    ),
)
def test_year_of_manufacture_reducer(firearm_details, output):
    assert year_of_manufacture_reducer(firearm_details) == output


@pytest.mark.parametrize(
    "firearm_details,output",
    (
        (
            {
                "is_onward_exported": False,
            },
            (("is-onward-exported", False),),
        ),
        (
            {
                "is_onward_exported": True,
                "is_onward_altered_processed": False,
                "is_onward_incorporated": False,
            },
            (
                ("is-onward-exported", True),
                ("is-altered", False),
                ("is-incorporated", False),
            ),
        ),
        (
            {
                "is_onward_exported": True,
                "is_onward_altered_processed": True,
                "is_onward_altered_processed_comments": "This is altered",
                "is_onward_incorporated": True,
                "is_onward_incorporated_comments": "This is incorporated",
            },
            (
                ("is-onward-exported", True),
                ("is-altered", True),
                ("is-altered-comments", "This is altered"),
                ("is-incorporated", True),
                ("is-incorporated-comments", "This is incorporated"),
            ),
        ),
    ),
)
def test_is_onward_exported_reducer(firearm_details, output):
    assert is_onward_exported_reducer(firearm_details) == output


@pytest.mark.parametrize(
    "firearm_details,output",
    (
        (
            {
                "is_deactivated": False,
            },
            (("is-deactivated", False),),
        ),
        (
            {
                "is_deactivated": True,
                "date_of_deactivation": "2020-10-09",
                "is_deactivated_to_standard": True,
            },
            (
                ("is-deactivated", True),
                ("deactivated-date", "2020-10-09"),
                ("is-proof-standards", True),
            ),
        ),
        (
            {
                "is_deactivated": True,
                "date_of_deactivation": "2020-10-09",
                "is_deactivated_to_standard": False,
                "not_deactivated_to_standard_comments": "Not deactivated to standard",
            },
            (
                ("is-deactivated", True),
                ("deactivated-date", "2020-10-09"),
                ("is-proof-standards", False),
                ("is-proof-standards-comments", "Not deactivated to standard"),
            ),
        ),
    ),
)
def test_is_deactivated_reducer(firearm_details, output):
    assert is_deactivated_reducer(firearm_details) == output


@pytest.mark.parametrize(
    "firearm_details,output",
    (
        (
            {
                "serial_numbers_available": SerialChoices.AVAILABLE.value,
                "serial_numbers": ["111", "222"],
            },
            (
                ("has-serial-numbers", SerialChoices.AVAILABLE.value),
                ("serial-numbers", ["111", "222"]),
            ),
        ),
        (
            {
                "serial_numbers_available": SerialChoices.LATER.value,
                "serial_numbers": ["111", "222"],
            },
            (
                ("has-serial-numbers", SerialChoices.LATER.value),
                ("serial-numbers", ["111", "222"]),
            ),
        ),
        (
            {
                "serial_numbers_available": SerialChoices.NOT_AVAILABLE.value,
            },
            (("has-serial-numbers", SerialChoices.NOT_AVAILABLE.value),),
        ),
        (
            {
                "serial_numbers_available": SerialChoices.NOT_AVAILABLE.value,
                "no_identification_markings_details": "No markings",
            },
            (
                ("has-serial-numbers", SerialChoices.NOT_AVAILABLE.value),
                ("no-identification-markings-details", "No markings"),
            ),
        ),
    ),
)
def test_serial_numbers_reducer(firearm_details, output):
    assert serial_numbers_reducer(firearm_details) == output
