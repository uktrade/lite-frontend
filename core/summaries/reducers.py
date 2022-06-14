from decimal import Decimal

from core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
)


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
    summary = (
        (
            "is-pv-graded",
            good["is_pv_graded"],
        ),
    )
    if good["is_pv_graded"]["key"] == "yes":
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


def firearm_on_application_reducer(good_on_application):
    firearm_details = good_on_application["firearm_details"]

    summary = (
        ("number-of-items", firearm_details["number_of_items"]),
        ("total-value", Decimal(good_on_application["value"])),
    )

    return summary


def firearms_act_section1_reducer(firearm_details):
    firearms_act_section = firearm_details.get("firearms_act_section")
    if not firearms_act_section:
        return ()

    if not firearms_act_section == FirearmsActSections.SECTION_1:
        return ()
