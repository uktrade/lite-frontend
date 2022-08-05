import datetime

from decimal import Decimal
from operator import itemgetter

from django.template.loader import get_template
from django.urls import reverse
from django.utils.formats import date_format
from django.utils.html import escape
from django.utils.safestring import mark_safe

from core.constants import (
    FirearmsActSections,
    SerialChoices,
)


FIREARM_LABELS = {
    "firearm-type": "Select the type of firearm product",
    "firearm-category": "Firearm category",
    "name": "Give the product a descriptive name",
    "calibre": "What is the calibre of the product?",
    "is-registered-firearms-dealer": "Are you a registered firearms dealer?",
    "rfd-certificate-document": "Upload a registered firearms dealer certificate",
    "rfd-certificate-reference-number": "Certificate reference number",
    "rfd-certificate-date-of-expiry": "Certificate date of expiry",
    "is-good-controlled": "Do you know the product's control list entry?",
    "assessed-control-list-entries": "Assessed control list entries",
    "control-list-entries": "Enter the control list entry",
    "is-pv-graded": "Does the product have a government security grading or classification?",
    "pv-grading-prefix": "Enter a prefix (optional)",
    "pv-grading-grading": "What is the security grading or classification?",
    "pv-grading-suffix": "Enter a suffix (optional)",
    "pv-grading-issuing-authority": "Name and address of the issuing authority",
    "pv-grading-details-reference": "Reference",
    "pv-grading-details-date-of-issue": "Date of issue",
    "is-replica": "Is the product a replica firearm?",
    "is-replica-description": "Describe the firearm the product is a replica of",
    "firearms-act-1968-section": "Which section of the Firearms Act 1968 is the product covered by?",
    "is-covered-by-firearm-act-section-one-two-or-five-explanation": "Explain",
    "has-product-document": "Do you have a document that shows what your product is and what it’s designed to do?",
    "no-product-document-explanation": "Explain why you are not able to upload a product document",
    "is-document-sensitive": "Is the document rated above Official-sensitive?",
    "product-document": "Upload a document that shows what your product is designed to do",
    "product-document-description": "Description (optional)",
    "is-covered-by-firearm-act-section-five": "Is the product covered by section 5 of the Firearms Act 1968?",
    "section-5-certificate-document": "Upload your section 5 letter of authority",
    "section-5-certificate-reference-number": "Certificate reference number",
    "section-5-certificate-date-of-expiry": "Certificate date of expiry",
    "section-5-certificate-missing": "Upload your section 5 letter of authority",
    "section-5-certificate-missing-reason": "Explain why you do not have a section 5 letter of authority",
}

PLATFORM_LABELS = {
    "name": "Give the product a descriptive name",
    "is-good-controlled": "Do you know the product's control list entry?",
    "control-list-entries": "Enter the control list entry",
    "is-pv-graded": "Does the product have a government security grading or classification?",
    "pv-grading-prefix": "Enter a prefix (optional)",
    "pv-grading-grading": "What is the security grading or classification?",
    "pv-grading-suffix": "Enter a suffix (optional)",
    "pv-grading-issuing-authority": "Name and address of the issuing authority",
    "pv-grading-details-reference": "Reference",
    "pv-grading-details-date-of-issue": "Date of issue",
    "has-product-document": "Do you have a document that shows what your product is and what it’s designed to do?",
    "no-product-document-explanation": "Explain why you are not able to upload a product document",
    "is-document-sensitive": "Is the document rated above Official-sensitive?",
    "product-document": "Upload a document that shows what your product is designed to do",
    "product-document-description": "Description (optional)",
}


def add_labels(summary, labels):
    labelled_summary = ()
    for key, *rest in summary:
        labelled_summary += ((key, *rest, labels.get(key, key)),)

    return labelled_summary


def key_value_formatter(key_value):
    return key_value["value"]


def identity(x):
    return x


def comma_separated_list(item_formatter=identity):
    def _comma_separated_list(iterable):
        if not iterable:
            return ""
        return ", ".join(item_formatter(i) for i in iterable)

    return _comma_separated_list


def yesno(boolean):
    return "Yes" if boolean else "No"


def to_date(val):
    return datetime.date.fromisoformat(val)


def date_formatter(format=None):
    def _date_formatter(val):
        return date_format(to_date(val), format)

    return _date_formatter


def mapping_formatter(map):
    def _mapping_formatter(val):
        return map.get(val, val)

    return _mapping_formatter


def just(val):
    def _just(_):
        return val

    return _just


def money_formatter(val):
    val = Decimal(val)
    return f"£{val:.2f}"


def model_choices_formatter(model_choice):
    def _model_choices_formatter(val):
        return model_choice[val].label

    return _model_choices_formatter


def template_formatter(template_name, context_generator):
    def _template_formatter(val):
        template = get_template(template_name)
        context = context_generator(val)
        return template.render(context)

    return _template_formatter


def organisation_document_formatter(document):
    url = reverse(
        "organisation:document",
        kwargs={
            "pk": document["id"],
        },
    )

    return document_formatter(document["document"], url)


FIREARM_VALUE_FORMATTERS = {
    "firearm-type": key_value_formatter,
    "firearm-category": comma_separated_list(key_value_formatter),
    "is-registered-firearms-dealer": yesno,
    "is-good-controlled": key_value_formatter,
    "control-list-entries": comma_separated_list(itemgetter("rating")),
    "assessed-control-list-entries": template_formatter(
        "goods/includes/assessed_control_list_entries.html",
        lambda val: {"assessed_control_list_entries": val},
    ),
    "is-pv-graded": mapping_formatter(
        {
            "yes": "Yes",
            "no": "No",
        }
    ),
    "pv-grading-grading": key_value_formatter,
    "pv-grading-details-date-of-issue": date_formatter("j F Y"),
    "is-replica": yesno,
    "has-product-document": yesno,
    "is-document-sensitive": yesno,
    "is-covered-by-firearm-act-section-five": mapping_formatter(
        {
            "Unsure": "Don't know",
        }
    ),
    "section-5-certificate-document": organisation_document_formatter,
    "section-5-certificate-date-of-expiry": date_formatter("j F Y"),
    "section-5-certificate-missing": just("I do not have a section 5 letter of authority"),
    "firearms-act-1968-section": mapping_formatter(
        {
            FirearmsActSections.SECTION_1: "Section 1",
            FirearmsActSections.SECTION_2: "Section 2",
            FirearmsActSections.SECTION_5: "Section 5",
            "Unsure": "Don't know",
        }
    ),
}


def format_values(summary, formatters):
    formatted_values_summary = ()
    for key, value, *rest in summary:
        formatter = formatters.get(key, identity)
        formatted_values_summary += ((key, formatter(value), *rest),)

    return formatted_values_summary


def document_formatter(document, url):
    if not document["safe"]:
        return document["name"]

    name = escape(document["name"])

    return mark_safe(  # nosec
        f'<a class="govuk-link govuk-link--no-visited-state" href="{url}" target="_blank">{name}</a>'
    )


FIREARM_ON_APPLICATION_FORMATTERS = {
    "firearm-certificate-missing": just("I do not have a firearm certificate"),
    "firearm-certificate-expiry-date": date_formatter("j F Y"),
    "shotgun-certificate-missing": just("I do not have a shotgun certificate"),
    "shotgun-certificate-expiry-date": date_formatter("j F Y"),
    "made-before-1938": yesno,
    "is-onward-exported": yesno,
    "is-altered": yesno,
    "is-incorporated": yesno,
    "is-deactivated": yesno,
    "deactivated-date": date_formatter("j F Y"),
    "is-proof-standards": yesno,
    "total-value": money_formatter,
    "has-serial-numbers": model_choices_formatter(SerialChoices),
}

FIREARM_ON_APPLICATION_LABELS = {
    "firearm-certificate": "Upload your firearm certificate",
    "firearm-certificate-missing": "Upload your firearm certificate",
    "firearm-certificate-missing-reason": "Explain why you do not have a firearm certificate",
    "firearm-certificate-number": "Certificate reference number",
    "firearm-certificate-expiry-date": "Certificate date of expiry",
    "shotgun-certificate": "Upload your shotgun certificate",
    "shotgun-certificate-missing": "Upload your shotgun certificate",
    "shotgun-certificate-missing-reason": "Explain why you do not have a shotgun certificate",
    "shotgun-certificate-number": "Certificate reference number",
    "shotgun-certificate-expiry-date": "Certificate date of expiry",
    "made-before-1938": "Was the product made before 1938?",
    "manufacture-year": "What year was it made?",
    "is-onward-exported": "Will the product be onward exported to any additional countries?",
    "is-altered": "Will the item be altered or processed before it is exported again?",
    "is-altered-comments": "Explain how the product will be processed or altered",
    "is-incorporated": "Will the product be incorporated into another item before it is onward exported?",
    "is-incorporated-comments": "Describe what you are incorporating the product into",
    "is-deactivated": "Has the product been deactivated?",
    "deactivated-date": "When was the item deactivated?",
    "is-proof-standards": "Has the item been deactivated to UK proof house standards?",
    "is-proof-standards-comments": "Describe who deactivated the product and to what standard it was done",
    "number-of-items": "Number of items",
    "total-value": "Total value",
    "has-serial-numbers": "Will each product have a serial number or other identification marking?",
    "no-identification-markings-details": "Explain why the product has not been marked",
    "serial-numbers": "Enter serial numbers or other identification markings",
}


PLATFORM_VALUE_FORMATTERS = {
    "is-good-controlled": key_value_formatter,
    "control-list-entries": comma_separated_list(itemgetter("rating")),
    "is-pv-graded": mapping_formatter(
        {
            "yes": "Yes",
            "no": "No",
        }
    ),
    "pv-grading-grading": key_value_formatter,
    "pv-grading-details-date-of-issue": date_formatter("j F Y"),
    "has-product-document": yesno,
    "is-document-sensitive": yesno,
}
