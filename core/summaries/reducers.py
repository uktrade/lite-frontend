from decimal import Decimal

from core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
    SerialChoices,
)
from core.goods.helpers import is_product_category_made_before_1938


def is_good_controlled_reducer(good):
    summary = (
        (
            "is-good-controlled",
            good["is_good_controlled"],
        ),
    )
    if good["is_good_controlled"]["key"] == "True":
        summary += (
            (
                "control-list-entries",
                good["control_list_entries"],
            ),
        )

    return summary


def is_pv_graded_reducer(good):
    is_pv_graded = good["is_pv_graded"]
    if isinstance(is_pv_graded, dict):
        is_pv_graded = is_pv_graded["key"]
    summary = (
        (
            "is-pv-graded",
            is_pv_graded,
        ),
    )
    if is_pv_graded == "yes":
        pv_grading_details = good["pv_grading_details"]
        if pv_grading_details["prefix"]:
            summary += (
                (
                    "pv-grading-prefix",
                    pv_grading_details["prefix"],
                ),
            )
        summary += (
            (
                "pv-grading-grading",
                pv_grading_details["grading"],
            ),
        )
        if pv_grading_details["suffix"]:
            summary += (
                (
                    "pv-grading-suffix",
                    pv_grading_details["suffix"],
                ),
            )
        summary += (
            (
                "pv-grading-issuing-authority",
                pv_grading_details["issuing_authority"],
            ),
            (
                "pv-grading-details-reference",
                pv_grading_details["reference"],
            ),
            (
                "pv-grading-details-date-of-issue",
                pv_grading_details["date_of_issue"],
            ),
        )

    return summary


def is_replica_reducer(firearm_details):
    summary = (
        (
            "is-replica",
            firearm_details["is_replica"],
        ),
    )
    if firearm_details["is_replica"]:
        summary += (("is-replica-description", firearm_details["replica_description"]),)

    return summary


def firearms_act_section5_reducer(firearm_details, organisation_documents):
    summary = ()
    if firearm_details["firearms_act_section"] == FirearmsActSections.SECTION_5:
        if firearm_details["section_certificate_missing"]:
            summary += (
                (
                    "section-5-certificate-missing",
                    True,
                ),
                (
                    "section-5-certificate-missing-reason",
                    firearm_details["section_certificate_missing_reason"],
                ),
            )
        else:
            summary += (
                (
                    "section-5-certificate-document",
                    organisation_documents[FirearmsActDocumentType.SECTION_5],
                ),
                (
                    "section-5-certificate-reference-number",
                    firearm_details["section_certificate_number"],
                ),
                (
                    "section-5-certificate-date-of-expiry",
                    firearm_details["section_certificate_date_of_expiry"],
                ),
            )

    return summary


def firearms_act_reducer(firearm_details, is_user_rfd, organisation_documents):
    if is_user_rfd:
        summary = (
            (
                "is-covered-by-firearm-act-section-five",
                firearm_details["is_covered_by_firearm_act_section_one_two_or_five"],
            ),
        )
        summary += firearms_act_section5_reducer(firearm_details, organisation_documents)
    elif firearm_details["is_covered_by_firearm_act_section_one_two_or_five"] == "Yes":
        summary = (
            (
                "firearms-act-1968-section",
                firearm_details["firearms_act_section"],
            ),
        )
        summary += firearms_act_section5_reducer(firearm_details, organisation_documents)
    elif firearm_details["is_covered_by_firearm_act_section_one_two_or_five_explanation"]:
        summary = (
            (
                "is-covered-by-firearm-act-section-one-two-or-five-explanation",
                firearm_details["is_covered_by_firearm_act_section_one_two_or_five_explanation"],
            ),
        )
    else:
        summary = ()

    return summary


def has_product_document_reducer(good):
    summary = (
        (
            "has-product-document",
            good["is_document_available"],
        ),
    )
    if good["is_document_available"]:
        summary += (
            (
                "is-document-sensitive",
                good["is_document_sensitive"],
            ),
        )
        if not good["is_document_sensitive"]:
            product_document = good["documents"][0]

            summary += (
                (
                    "product-document",
                    product_document,
                ),
                (
                    "product-document-description",
                    product_document["description"],
                ),
            )
    else:
        summary += (
            (
                "no-product-document-explanation",
                good["no_document_comments"],
            ),
        )

    return summary


def firearm_reducer(good, is_user_rfd, organisation_documents):
    firearm_details = good["firearm_details"]

    summary = (
        (
            "firearm-type",
            firearm_details["type"],
        ),
        (
            "firearm-category",
            firearm_details["category"],
        ),
        (
            "name",
            good["name"],
        ),
        (
            "calibre",
            firearm_details["calibre"],
        ),
        (
            "is-registered-firearms-dealer",
            is_user_rfd,
        ),
    )

    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += is_replica_reducer(firearm_details)
    summary += firearms_act_reducer(firearm_details, is_user_rfd, organisation_documents)
    summary += has_product_document_reducer(good)

    return summary


def firearm_on_application_reducer(good_on_application, good_on_application_documents):
    firearm_details = good_on_application["firearm_details"]

    summary = (
        ("number-of-items", firearm_details["number_of_items"]),
        ("total-value", Decimal(good_on_application["value"])),
    )

    summary += firearms_act_section1_reducer(firearm_details, good_on_application_documents)
    summary += firearms_act_section2_reducer(firearm_details, good_on_application_documents)
    summary += year_of_manufacture_reducer(firearm_details)
    summary += is_onward_exported_reducer(firearm_details)
    summary += is_deactivated_reducer(firearm_details)
    summary += serial_numbers_reducer(firearm_details)

    return summary


def firearms_act_section1_reducer(firearm_details, good_on_application_documents):
    firearms_act_section = firearm_details.get("firearms_act_section")
    if not firearms_act_section:
        return ()

    if not firearms_act_section == FirearmsActSections.SECTION_1:
        return ()

    if firearm_details["section_certificate_missing"]:
        return (
            ("firearm-certificate-missing", True),
            ("firearm-certificate-missing-reason", firearm_details["section_certificate_missing_reason"]),
        )

    return (
        ("firearm-certificate", good_on_application_documents[FirearmsActDocumentType.SECTION_1]),
        ("firearm-certificate-expiry-date", firearm_details["section_certificate_date_of_expiry"]),
        ("firearm-certificate-number", firearm_details["section_certificate_number"]),
    )


def firearms_act_section2_reducer(firearm_details, good_on_application_documents):
    firearms_act_section = firearm_details.get("firearms_act_section")
    if not firearms_act_section:
        return ()

    if not firearms_act_section == FirearmsActSections.SECTION_2:
        return ()

    if firearm_details["section_certificate_missing"]:
        return (
            ("shotgun-certificate-missing", True),
            ("shotgun-certificate-missing-reason", firearm_details["section_certificate_missing_reason"]),
        )

    return (
        ("shotgun-certificate", good_on_application_documents[FirearmsActDocumentType.SECTION_2]),
        ("shotgun-certificate-expiry-date", firearm_details["section_certificate_date_of_expiry"]),
        ("shotgun-certificate-number", firearm_details["section_certificate_number"]),
    )


def year_of_manufacture_reducer(firearm_details):
    summary = ()

    is_made_before_1938 = firearm_details.get("is_made_before_1938")
    if is_made_before_1938 is not None:
        summary += (("made-before-1938", is_made_before_1938),)

    if is_made_before_1938 or is_made_before_1938 is None or is_product_category_made_before_1938(firearm_details):
        summary += (("manufacture-year", firearm_details["year_of_manufacture"]),)

    return summary


def is_onward_exported_reducer(firearm_details):
    summary = (("is-onward-exported", firearm_details["is_onward_exported"]),)
    if firearm_details["is_onward_exported"]:
        summary += (("is-altered", firearm_details["is_onward_altered_processed"]),)
        if firearm_details["is_onward_altered_processed"]:
            summary += (("is-altered-comments", firearm_details["is_onward_altered_processed_comments"]),)
        summary += (("is-incorporated", firearm_details["is_onward_incorporated"]),)
        if firearm_details["is_onward_incorporated"]:
            summary += (("is-incorporated-comments", firearm_details["is_onward_incorporated_comments"]),)
    return summary


def is_deactivated_reducer(firearm_details):
    summary = (("is-deactivated", firearm_details["is_deactivated"]),)
    if firearm_details["is_deactivated"]:
        summary += (
            ("deactivated-date", firearm_details["date_of_deactivation"]),
            ("is-proof-standards", firearm_details["is_deactivated_to_standard"]),
        )
        if not firearm_details["is_deactivated_to_standard"]:
            summary += (("is-proof-standards-comments", firearm_details["not_deactivated_to_standard_comments"]),)
    return summary


def serial_numbers_reducer(firearm_details):
    summary = (("has-serial-numbers", firearm_details["serial_numbers_available"]),)

    if firearm_details["serial_numbers_available"] in [SerialChoices.AVAILABLE, SerialChoices.LATER]:
        summary += (("serial-numbers", firearm_details["serial_numbers"]),)

    if firearm_details["serial_numbers_available"] == SerialChoices.NOT_AVAILABLE and firearm_details.get(
        "no_identification_markings_details"
    ):
        summary += (("no-identification-markings-details", firearm_details["no_identification_markings_details"]),)

    return summary
