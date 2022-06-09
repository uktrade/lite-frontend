import datetime

from operator import itemgetter

from django.urls import reverse
from django.utils.formats import date_format
from django.utils.html import escape
from django.utils.safestring import mark_safe


FIREARM_LABELS = {
    "firearm-type": "Select the type of firearm product",
    "firearm-category": "Firearm category",
    "name": "Give the product a descriptive name",
    "calibre": "What is the calibre of the product?",
    "is-registered-firearms-dealer": "Are you a registered firearms dealer?",
    "is-good-controlled": "Do you know the product's control list entry?",
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
    "is-pv-graded": key_value_formatter,
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
