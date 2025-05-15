from decimal import Decimal

from core.constants import (
    COMPONENT_DETAILS_MAP,
    FirearmsActDocumentType,
    FirearmsActSections,
    OrganisationDocumentType,
    SerialChoices,
)
from core.goods.helpers import is_product_category_made_before_1938


def _get_assessed_control_list_item(precedent):
    return (
        precedent["control_list_entries"],
        precedent["destinations"],
        precedent["goods_starting_point"],
    )


def _filter_duplicate_assessed_items(assessed_items):
    seen = set()
    for assessed_item in assessed_items:
        cles, destinations, origin = assessed_item
        current = frozenset((frozenset(cles), frozenset(destinations), origin))
        if current in seen:
            continue
        seen.add(current)
        yield assessed_item


def is_good_controlled_reducer(good):
    is_good_controlled = good["is_good_controlled"]["key"] == "True"
    if not is_good_controlled:
        return (
            (
                "is-good-controlled",
                good["is_good_controlled"],
            ),
        )

    precedents = good.get("precedents")
    if precedents:
        assessed_items = (_get_assessed_control_list_item(precedent) for precedent in precedents)
        assessed_items = _filter_duplicate_assessed_items(assessed_items)
        return (
            (
                "assessed-control-list-entries",
                tuple([i for i in assessed_items]),
            ),
        )

    return (
        (
            "is-good-controlled",
            good["is_good_controlled"],
        ),
        (
            "control-list-entries",
            good["control_list_entries"],
        ),
    )


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
            section_5_certificate_document = organisation_documents[FirearmsActDocumentType.SECTION_5]
            summary += (
                (
                    "section-5-certificate-document",
                    section_5_certificate_document,
                ),
                (
                    "section-5-certificate-reference-number",
                    section_5_certificate_document["reference_code"],
                ),
                (
                    "section-5-certificate-date-of-expiry",
                    section_5_certificate_document["expiry_date"],
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
                "firearms-act-1968-section",
                firearm_details["is_covered_by_firearm_act_section_one_two_or_five"],
            ),
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
        if good.get("product_description"):
            summary += (("product-description", good["product_description"]),)

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

    summary += rfd_reducer(is_user_rfd, organisation_documents)
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += is_replica_reducer(firearm_details)
    summary += firearms_act_reducer(firearm_details, is_user_rfd, organisation_documents)
    summary += has_product_document_reducer(good)

    return summary


def components_for_firearms_reducer(good, is_user_rfd, organisation_documents):
    firearm_details = good["firearm_details"]

    summary = (
        (
            "firearm-type",
            firearm_details["type"],
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

    summary += part_number_reducer(good)
    summary += rfd_reducer(is_user_rfd, organisation_documents)
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += is_replica_reducer(firearm_details)
    summary += firearms_act_reducer(firearm_details, is_user_rfd, organisation_documents)
    summary += has_product_document_reducer(good)

    return summary


def firearms_accessory_reducer(good):
    firearm_details = good["firearm_details"]

    summary = (
        (
            "firearm-type",
            firearm_details["type"],
        ),
        (
            "name",
            good["name"],
        ),
    )

    summary += part_number_reducer(good)
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += product_component_reducer(good)
    summary += uses_information_security_reducer(good)
    summary += designed_for_military_use_reducer(good)
    summary += has_product_document_reducer(good)

    return summary


def software_related_to_firearms_reducer(good):
    firearm_details = good["firearm_details"]

    summary = (
        (
            "firearm-type",
            firearm_details["type"],
        ),
        (
            "name",
            good["name"],
        ),
    )

    summary += part_number_reducer(good)
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += uses_information_security_reducer(good)
    summary += designed_for_military_use_reducer(good)
    summary += has_product_document_reducer(good)

    return summary


def technology_related_to_firearms_reducer(good):
    firearm_details = good["firearm_details"]

    summary = (
        (
            "firearm-type",
            firearm_details["type"],
        ),
        (
            "name",
            good["name"],
        ),
    )

    summary += part_number_reducer(good)
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += uses_information_security_reducer(good)
    summary += designed_for_military_use_reducer(good)
    summary += has_product_document_reducer(good)

    return summary


def firearm_ammunition_reducer(good, is_user_rfd, organisation_documents):
    firearm_details = good["firearm_details"]

    summary = (
        (
            "firearm-type",
            firearm_details["type"],
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

    summary += rfd_reducer(is_user_rfd, organisation_documents)
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += is_replica_reducer(firearm_details)
    summary += firearms_act_reducer(firearm_details, is_user_rfd, organisation_documents)
    summary += has_product_document_reducer(good)

    return summary


def rfd_reducer(is_user_rfd, organisation_documents):
    if not is_user_rfd or not organisation_documents.get(OrganisationDocumentType.RFD_CERTIFICATE):
        return ()

    rfd_certificate_document = organisation_documents[OrganisationDocumentType.RFD_CERTIFICATE]

    summary = (
        (
            "rfd-certificate-document",
            rfd_certificate_document,
        ),
        (
            "rfd-certificate-reference-number",
            rfd_certificate_document["reference_code"],
        ),
        (
            "rfd-certificate-date-of-expiry",
            rfd_certificate_document["expiry_date"],
        ),
    )

    return summary


def firearm_on_application_reducer(good_on_application, good_on_application_documents):
    firearm_details = good_on_application["firearm_details"]

    summary = ()

    summary += quantity_and_value_reducer(good_on_application)
    summary += firearms_act_section1_reducer(firearm_details, good_on_application_documents)
    summary += firearms_act_section2_reducer(firearm_details, good_on_application_documents)
    summary += year_of_manufacture_reducer(firearm_details)
    summary += is_onward_exported_reducer(good_on_application)
    summary += is_deactivated_reducer(firearm_details)
    summary += serial_numbers_reducer(firearm_details)

    return summary


def quantity_and_value_reducer(good_on_application):
    if not good_on_application["value"]:
        return (("no-set-quantities-or-value", True),)

    quantity = good_on_application["quantity"]
    if good_on_application["unit"]["key"] == "NAR":
        quantity = int(quantity)

    summary = (
        ("number-of-items", quantity),
        ("total-value", Decimal(good_on_application["value"])),
    )

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


def is_onward_exported_reducer(onward_exported_object):
    summary = (("is-onward-exported", onward_exported_object["is_onward_exported"]),)
    if onward_exported_object["is_onward_exported"]:
        summary += (("is-altered", onward_exported_object["is_onward_altered_processed"]),)
        if onward_exported_object["is_onward_altered_processed"]:
            summary += (("is-altered-comments", onward_exported_object["is_onward_altered_processed_comments"]),)
        summary += (("is-incorporated", onward_exported_object["is_onward_incorporated"]),)
        if onward_exported_object["is_onward_incorporated"]:
            summary += (("is-incorporated-comments", onward_exported_object["is_onward_incorporated_comments"]),)
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
    if firearm_details["serial_numbers_available"] is None:
        return ()

    summary = (("has-serial-numbers", firearm_details["serial_numbers_available"]),)

    if firearm_details["serial_numbers_available"] in [SerialChoices.AVAILABLE, SerialChoices.LATER]:
        summary += (("serial-numbers", firearm_details["serial_numbers"]),)

    if firearm_details["serial_numbers_available"] == SerialChoices.NOT_AVAILABLE and firearm_details.get(
        "no_identification_markings_details"
    ):
        summary += (("no-identification-markings-details", firearm_details["no_identification_markings_details"]),)

    return summary


def uses_information_security_reducer(good):
    if not good["uses_information_security"]:
        return (("uses-information-security", False),)

    return (
        ("uses-information-security", True),
        ("uses-information-security-details", good["information_security_details"]),
    )


def component_accessory_details_reducer(good):
    is_component_key = good.get("is_component", {}).get("key")
    if not is_component_key or is_component_key == "no":
        return (("is-component", False),)
    else:
        return (
            ("is-component", True),
            (COMPONENT_DETAILS_MAP[is_component_key].replace("_", "-"), good["component_details"]),
            ("component-type", is_component_key),
        )


def part_number_reducer(good):
    no_part_number_comments = good.get("no_part_number_comments")
    if no_part_number_comments:
        return (
            ("has-part-number", False),
            ("no-part-number-comments", no_part_number_comments),
        )
    return (("part-number", good["part_number"]),)


def product_component_reducer(good):
    return (("product-component", good["is_component"]["value"]),)


def complete_item_reducer(good):
    summary = (
        (
            "is-firearm-product",
            False,
        ),
        (
            "product-category",
            "complete_item",
        ),
        (
            "name",
            good["name"],
        ),
    )
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += uses_information_security_reducer(good)
    summary += has_product_document_reducer(good)
    summary += part_number_reducer(good)
    summary += designed_for_military_use_reducer(good)

    return summary


def component_accessory_reducer(good):
    summary = (
        (
            "is-firearm-product",
            False,
        ),
        (
            "product-category",
            "component",
        ),
        (
            "is-material-substance",
            False,
        ),
        (
            "name",
            good["name"],
        ),
    )
    summary += component_accessory_details_reducer(good)
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += uses_information_security_reducer(good)
    summary += has_product_document_reducer(good)
    summary += part_number_reducer(good)
    summary += designed_for_military_use_reducer(good)

    return summary


def material_reducer(good):
    summary = (
        (
            "is-firearm-product",
            False,
        ),
        (
            "product-category",
            "material",
        ),
        (
            "is-material-substance",
            True,
        ),
        (
            "name",
            good["name"],
        ),
    )
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += has_product_document_reducer(good)
    summary += part_number_reducer(good)
    summary += designed_for_military_use_reducer(good)

    return summary


def complete_item_on_application_reducer(good_on_application):
    summary = ()
    summary += quantity_and_value_reducer(good_on_application)
    summary += is_onward_exported_reducer(good_on_application)
    return summary


def material_on_application_reducer(good_on_application):
    summary = (
        ("unit", good_on_application["unit"]["value"]),
        ("quantity", good_on_application["quantity"]),
        ("total-value", Decimal(good_on_application["value"])),
    )
    summary += is_onward_exported_reducer(good_on_application)
    return summary


def component_accessory_on_application_reducer(good_on_application):
    summary = ()
    summary += quantity_and_value_reducer(good_on_application)
    summary += is_onward_exported_reducer(good_on_application)
    return summary


def technology_reducer(good):
    summary = (
        (
            "is-firearm-product",
            False,
        ),
        ("non-firearm-category", "It helps to operate a product"),
        (
            "name",
            good["name"],
        ),
    )
    summary += is_good_controlled_reducer(good)
    summary += is_pv_graded_reducer(good)
    summary += has_product_document_reducer(good)
    summary += part_number_reducer(good)
    summary += security_features_reducer(good)
    summary += declared_at_customs_reducer(good)
    summary += designed_for_military_use_reducer(good)
    return summary


def security_features_reducer(good):
    if good.get("has_security_features"):
        return (
            ("security-features", True),
            ("security-feature-details", good["security_feature_details"]),
        )

    return (("security-features", False),)


def declared_at_customs_reducer(good):
    if good.get("has_declared_at_customs"):
        return (("declared-at-customs", True),)

    return (("declared-at-customs", False),)


def designed_for_military_use_reducer(good):
    is_military_use_key = good["is_military_use"]["key"]

    summary = (("military-use", is_military_use_key),)
    if is_military_use_key == "yes_modified":
        summary += (("military-use-details", good["modified_military_use_details"]),)

    return summary


def technology_on_application_reducer(good_on_application):
    summary = ()
    summary += quantity_and_value_reducer(good_on_application)
    summary += is_onward_exported_reducer(good_on_application)
    return summary
