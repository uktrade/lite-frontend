import pytest

from core.summaries.reducers import (
    firearm_reducer,
    firearms_act_reducer,
    firearms_act_section5_reducer,
    has_product_document_reducer,
    is_good_controlled_reducer,
    is_pv_graded_reducer,
    is_replica_reducer,
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
    output = (
        ("firearm-type", "firearm-details-type"),
        ("firearm-category", "firearm-details-category"),
        ("name", "good-name"),
        ("calibre", "firearm-details-calibre"),
        ("is-registered-firearms-dealer", is_user_rfd),
    )
    assert firearm_reducer(good, is_user_rfd, organisation_documents) == output

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
                ("is-pv-graded", {"key": "yes"}),
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
                ("is-pv-graded", {"key": "yes"}),
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
            (("is-pv-graded", {"key": "no"}),),
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
                "no_documents_comments": "No document comments",
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
