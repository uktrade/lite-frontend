from core.constants import (
    FirearmsProductType,
    ProductCategories,
)
from core.helpers import is_good_on_application_product_type
from core.summaries.formatters import (
    add_labels,
    format_values,
    FIREARM_LABELS,
    FIREARM_ON_APPLICATION_FORMATTERS,
    FIREARM_ON_APPLICATION_LABELS,
    FIREARM_VALUE_FORMATTERS,
    FIREARMS_ACCESSORY_VALUE_FORMATTERS,
    template_formatter,
    COMPLETE_ITEM_LABELS,
    COMPLETE_ITEM_VALUE_FORMATTERS,
    COMPLETE_ITEM_ON_APPLICATION_FORMATTERS,
    COMPLETE_ITEM_ON_APPLICATION_LABELS,
    FIREARMS_ACCESSORY_LABELS,
    TECHNOLOGY_LABELS,
    TECHNOLOGY_VALUE_FORMATTERS,
    TECHNOLOGY_ON_APPLICATION_FORMATTERS,
    TECHNOLOGY_ON_APPLICATION_LABELS,
    MATERIAL_LABELS,
    MATERIAL_VALUE_FORMATTERS,
    MATERIAL_ON_APPLICATION_FORMATTERS,
    MATERIAL_ON_APPLICATION_LABELS,
    COMPONENT_ACCESSORY_LABELS,
    COMPONENT_ACCESSORY_VALUE_FORMATTERS,
    COMPONENT_ACCESSORY_ON_APPLICATION_FORMATTERS,
    COMPONENT_ACCESSORY_ON_APPLICATION_LABELS,
    SOFTWARE_RELATED_TO_FIREARMS_LABELS,
    SOFTWARE_RELATED_TO_FIREARMS_VALUE_FORMATTERS,
)
from core.summaries.reducers import (
    firearm_on_application_reducer,
    firearm_reducer,
    firearm_ammunition_reducer,
    components_for_firearms_reducer,
    complete_item_on_application_reducer,
    complete_item_reducer,
    technology_on_application_reducer,
    technology_reducer,
    material_reducer,
    material_on_application_reducer,
    component_accessory_on_application_reducer,
    component_accessory_reducer,
    software_related_to_firearms_reducer,
)
from core.summaries.utils import pick_fields

FIREARM_FIELDS = (
    "firearm-type",
    "firearm-category",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "assessed-control-list-entries",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "calibre",
    "is-replica",
    "is-replica-description",
    "is-registered-firearms-dealer",
    "rfd-certificate-document",
    "rfd-certificate-reference-number",
    "rfd-certificate-date-of-expiry",
    "is-covered-by-firearm-act-section-five",
    "firearms-act-1968-section",
    "is-covered-by-firearm-act-section-one-two-or-five-explanation",
    "section-5-certificate-document",
    "section-5-certificate-reference-number",
    "section-5-certificate-date-of-expiry",
    "section-5-certificate-missing",
    "section-5-certificate-missing-reason",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
)

COMPONENTS_FOR_FIREARMS_FIELDS = (
    "firearm-type",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "assessed-control-list-entries",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "calibre",
    "is-replica",
    "is-replica-description",
    "is-registered-firearms-dealer",
    "rfd-certificate-document",
    "rfd-certificate-reference-number",
    "rfd-certificate-date-of-expiry",
    "is-covered-by-firearm-act-section-five",
    "firearms-act-1968-section",
    "is-covered-by-firearm-act-section-one-two-or-five-explanation",
    "section-5-certificate-document",
    "section-5-certificate-reference-number",
    "section-5-certificate-date-of-expiry",
    "section-5-certificate-missing",
    "section-5-certificate-missing-reason",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
)

FIREARM_AMMUNITION_FIELDS = (
    "firearm-type",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "assessed-control-list-entries",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "calibre",
    "is-replica",
    "is-replica-description",
    "is-registered-firearms-dealer",
    "rfd-certificate-document",
    "rfd-certificate-reference-number",
    "rfd-certificate-date-of-expiry",
    "is-covered-by-firearm-act-section-five",
    "firearms-act-1968-section",
    "is-covered-by-firearm-act-section-one-two-or-five-explanation",
    "section-5-certificate-document",
    "section-5-certificate-reference-number",
    "section-5-certificate-date-of-expiry",
    "section-5-certificate-missing",
    "section-5-certificate-missing-reason",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
)

FIREARMS_ACCESSORY_FIELDS = (
    "firearm-type",
    "name",
    "part-number",
    "is-good-controlled",
    "control-list-entries",
    "assessed-control-list-entries",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
    "uses-information-security",
    "uses-information-security-details",
    "military-use",
    "military-use-details",
)

SOFTWARE_RELATED_TO_FIREARMS_FIELDS = (
    "firearm-type",
    "name",
    "part-number",
    "is-good-controlled",
    "control-list-entries",
    "assessed-control-list-entries",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
    "general-details",
    "uses-information-security",
    "uses-information-security-details",
    "military-use",
    "military-use-details",
)

COMPLETE_ITEM_FIELDS = (
    "is-firearm-product",
    "product-category",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "part-number",
    "has-part-number",
    "no-part-number-comments",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "uses-information-security",
    "uses-information-security-details",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
    "military-use",
    "military-use-details",
)

MATERIAL_FIELDS = (
    "is-firearm-product",
    "product-category",
    "is-material-substance",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "part-number",
    "has-part-number",
    "no-part-number-comments",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
    "military-use",
    "military-use-details",
)

TECHNOLOGY_FIELDS = (
    "is-firearm-product",
    "non-firearm-category",
    "name",
    "is-good-controlled",
    "control-list-entries",
    "part-number",
    "has-part-number",
    "no-part-number-comments",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "security-features",
    "security-feature-details",
    "declared-at-customs",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
    "military-use",
    "military-use-details",
)

COMPONENT_ACCESSORY_FIELDS = (
    "is-firearm-product",
    "product-category",
    "is-material-substance",
    "name",
    "is-component",
    "component-type",
    "component-details",
    "designed-details",
    "modified-details",
    "general-details",
    "is-good-controlled",
    "control-list-entries",
    "part-number",
    "has-part-number",
    "no-part-number-comments",
    "is-pv-graded",
    "pv-grading-prefix",
    "pv-grading-grading",
    "pv-grading-suffix",
    "pv-grading-issuing-authority",
    "pv-grading-details-reference",
    "pv-grading-details-date-of-issue",
    "uses-information-security",
    "uses-information-security-details",
    "has-product-document",
    "no-product-document-explanation",
    "product-description",
    "is-document-sensitive",
    "product-document",
    "product-document-description",
    "military-use",
    "military-use-details",
)


def firearm_summary(good, is_user_rfd, organisation_documents, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = firearm_reducer(good, is_user_rfd, organisation_documents)
    formatters = {
        **FIREARM_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, FIREARM_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARM_LABELS)

    return summary


def components_for_firearms_summary(good, is_user_rfd, organisation_documents, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = components_for_firearms_reducer(good, is_user_rfd, organisation_documents)
    formatters = {
        **FIREARM_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, COMPONENTS_FOR_FIREARMS_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARM_LABELS)

    return summary


def firearm_ammunition_summary(good, is_user_rfd, organisation_documents, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = firearm_ammunition_reducer(good, is_user_rfd, organisation_documents)
    formatters = {
        **FIREARM_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, FIREARM_AMMUNITION_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARM_LABELS)

    return summary


def components_for_firearms_ammunition_summary(good, is_user_rfd, organisation_documents, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = components_for_firearms_reducer(good, is_user_rfd, organisation_documents)
    formatters = {
        **FIREARM_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, COMPONENTS_FOR_FIREARMS_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARM_LABELS)

    return summary


def firearms_accessory_summary(good, is_user_rfd, organisation_documents, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = components_for_firearms_reducer(good, is_user_rfd, organisation_documents)
    formatters = {
        **FIREARMS_ACCESSORY_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, FIREARMS_ACCESSORY_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARMS_ACCESSORY_LABELS)

    return summary


def software_related_to_firearms_summary(good, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = software_related_to_firearms_reducer(good)
    formatters = {
        **SOFTWARE_RELATED_TO_FIREARMS_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, SOFTWARE_RELATED_TO_FIREARMS_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, SOFTWARE_RELATED_TO_FIREARMS_LABELS)

    return summary


FIREARM_ON_APPLICATION_FIELDS = (
    "firearm-certificate",
    "firearm-certificate-missing",
    "firearm-certificate-missing-reason",
    "firearm-certificate-number",
    "firearm-certificate-expiry-date",
    "shotgun-certificate",
    "shotgun-certificate-missing",
    "shotgun-certificate-missing-reason",
    "shotgun-certificate-number",
    "shotgun-certificate-expiry-date",
    "made-before-1938",
    "manufacture-year",
    "is-onward-exported",
    "is-altered",
    "is-altered-comments",
    "is-incorporated",
    "is-incorporated-comments",
    "is-deactivated",
    "deactivated-date",
    "is-proof-standards",
    "is-proof-standards-comments",
    "number-of-items",
    "total-value",
    "has-serial-numbers",
    "no-identification-markings-details",
    "serial-numbers",
)


def firearm_on_application_summary(good_on_application, good_on_application_documents, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = firearm_on_application_reducer(good_on_application, good_on_application_documents)

    def serial_numbers_formatter(serial_numbers):
        return template_formatter(
            "goods/includes/serial_numbers.html",
            lambda _: good_on_application,
        )(serial_numbers)

    formatters = {
        **FIREARM_ON_APPLICATION_FORMATTERS,
        **{
            "serial-numbers": serial_numbers_formatter,
        },
        **additional_formatters,
    }

    summary = pick_fields(summary, FIREARM_ON_APPLICATION_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, FIREARM_ON_APPLICATION_LABELS)

    return summary


COMPLETE_ITEM_ON_APPLICATION_FIELDS = (
    "is-onward-exported",
    "is-altered",
    "is-altered-comments",
    "is-incorporated",
    "is-incorporated-comments",
    "number-of-items",
    "total-value",
)


def complete_item_summary(good, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = complete_item_reducer(good)
    formatters = {
        **COMPLETE_ITEM_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, COMPLETE_ITEM_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, COMPLETE_ITEM_LABELS)

    return summary


def complete_item_product_on_application_summary(good_on_application, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = complete_item_on_application_reducer(good_on_application)
    formatters = {
        **COMPLETE_ITEM_ON_APPLICATION_FORMATTERS,
        **additional_formatters,
    }

    summary = pick_fields(summary, COMPLETE_ITEM_ON_APPLICATION_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, COMPLETE_ITEM_ON_APPLICATION_LABELS)

    return summary


MATERIAL_ON_APPLICATION_FIELDS = (
    "is-onward-exported",
    "is-altered",
    "is-altered-comments",
    "is-incorporated",
    "is-incorporated-comments",
    "unit",
    "quantity",
    "total-value",
)


def material_summary(good, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = material_reducer(good)
    formatters = {
        **MATERIAL_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, MATERIAL_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, MATERIAL_LABELS)

    return summary


def material_product_on_application_summary(good_on_application, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = material_on_application_reducer(good_on_application)
    formatters = {
        **MATERIAL_ON_APPLICATION_FORMATTERS,
        **additional_formatters,
    }

    summary = pick_fields(summary, MATERIAL_ON_APPLICATION_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, MATERIAL_ON_APPLICATION_LABELS)

    return summary


TECHNOLOGY_ON_APPLICATION_FIELDS = (
    "is-onward-exported",
    "is-altered",
    "is-altered-comments",
    "is-incorporated",
    "is-incorporated-comments",
    "number-of-items",
    "total-value",
)


def technology_summary(good, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = technology_reducer(good)
    formatters = {
        **TECHNOLOGY_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, TECHNOLOGY_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, TECHNOLOGY_LABELS)

    return summary


def technology_product_on_application_summary(good_on_application, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = technology_on_application_reducer(good_on_application)
    formatters = {
        **TECHNOLOGY_ON_APPLICATION_FORMATTERS,
        **additional_formatters,
    }

    summary = pick_fields(summary, TECHNOLOGY_ON_APPLICATION_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, TECHNOLOGY_ON_APPLICATION_LABELS)

    return summary


COMPONENT_ACCESSORY_ON_APPLICATION_FIELDS = (
    "is-onward-exported",
    "is-altered",
    "is-altered-comments",
    "is-incorporated",
    "is-incorporated-comments",
    "number-of-items",
    "total-value",
)


def component_accessory_summary(good, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}
    summary = component_accessory_reducer(good)
    formatters = {
        **COMPONENT_ACCESSORY_VALUE_FORMATTERS,
        **additional_formatters,
    }
    summary = pick_fields(summary, COMPONENT_ACCESSORY_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, COMPONENT_ACCESSORY_LABELS)

    return summary


def component_accessory_product_on_application_summary(good_on_application, additional_formatters=None):
    if not additional_formatters:
        additional_formatters = {}

    summary = component_accessory_on_application_reducer(good_on_application)
    formatters = {
        **COMPONENT_ACCESSORY_ON_APPLICATION_FORMATTERS,
        **additional_formatters,
    }

    summary = pick_fields(summary, COMPONENT_ACCESSORY_ON_APPLICATION_FIELDS)
    summary = format_values(summary, formatters)
    summary = add_labels(summary, COMPONENT_ACCESSORY_ON_APPLICATION_LABELS)

    return summary


class NoSummaryForType(Exception):
    pass


class SummaryTypes:
    FIREARM = "FIREARM"
    COMPONENTS_FOR_FIREARMS = "COMPONENTS_FOR_FIREARMS"
    FIREARM_AMMUNITION = "FIREARM_AMMUNITION"
    COMPONENTS_FOR_FIREARMS_AMMUNITION = "COMPONENTS_FOR_FIREARMS_AMMUNITION"
    FIREARMS_ACCESSORY = "FIREARMS_ACCESSORY"
    SOFTWARE_RELATED_TO_FIREARMS = "SOFTWARE_RELATED_TO_FIREARMS"
    COMPLETE_ITEM = "COMPLETE_ITEM"
    MATERIAL = "MATERIAL"
    TECHNOLOGY = "TECHNOLOGY"
    COMPONENT_ACCESSORY = "COMPONENT_ACCESSORY"


def get_summary_type_from_item_category(item_category):
    summary_map = {
        ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM: SummaryTypes.COMPLETE_ITEM,
        ProductCategories.PRODUCT_CATEGORY_MATERIAL: SummaryTypes.MATERIAL,
        ProductCategories.PRODUCT_CATEGORY_SOFTWARE: SummaryTypes.TECHNOLOGY,
        ProductCategories.PRODUCT_CATEGORY_COMPONENT_ACCESSORY: SummaryTypes.COMPONENT_ACCESSORY,
    }

    try:
        return summary_map[item_category]
    except KeyError as e:
        raise NoSummaryForType(f"Did not find summary for product category {item_category}") from e


def get_summary_type_for_good(good):
    firearm_details = good.get("firearm_details")
    if firearm_details:
        if firearm_details["type"]["key"] == FirearmsProductType.FIREARMS:
            return SummaryTypes.FIREARM
        if firearm_details["type"]["key"] == FirearmsProductType.COMPONENTS_FOR_FIREARMS:
            return SummaryTypes.COMPONENTS_FOR_FIREARMS
        if firearm_details["type"]["key"] == FirearmsProductType.AMMUNITION:
            return SummaryTypes.FIREARM_AMMUNITION
        if firearm_details["type"]["key"] == FirearmsProductType.COMPONENTS_FOR_AMMUNITION:
            return SummaryTypes.COMPONENTS_FOR_FIREARMS_AMMUNITION
        if firearm_details["type"]["key"] == FirearmsProductType.FIREARMS_ACCESSORY:
            return SummaryTypes.FIREARMS_ACCESSORY
        if firearm_details["type"]["key"] == FirearmsProductType.SOFTWARE_RELATED_TO_FIREARM:
            return SummaryTypes.SOFTWARE_RELATED_TO_FIREARMS
        raise NoSummaryForType

    item_category = good.get("item_category")
    if not item_category:
        raise NoSummaryForType

    item_category = item_category["key"]

    return get_summary_type_from_item_category(item_category)


def get_summary_type_for_good_on_application(good_on_application):
    if is_good_on_application_product_type(good_on_application, FirearmsProductType.FIREARMS):
        return SummaryTypes.FIREARM

    if good_on_application.get("firearm_details"):
        raise NoSummaryForType("Missing `firearm_details`")

    good = good_on_application.get("good")
    if not good:
        raise NoSummaryForType("Missing `good`")

    item_category = good.get("item_category")
    if not item_category:
        raise NoSummaryForType("Missing `item_category`")

    item_category = item_category["key"]

    return get_summary_type_from_item_category(item_category)
