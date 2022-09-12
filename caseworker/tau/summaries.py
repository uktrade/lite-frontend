from core.summaries.utils import remove_fields

from caseworker.cases.helpers.summaries import get_good_on_application_summary


def get_good_on_application_tau_summary(*args, **kwargs):
    summary = get_good_on_application_summary(*args, **kwargs)
    if not summary:
        return None

    summary = remove_fields(
        summary,
        [
            "name",
            "is-good-controlled",
            "control-list-entries",
            "has-product-document",
            "is-document-sensitive",
            "no-product-document-explanation",
            "product-document",
            "product-document-description",
            "product-description",
        ],
    )

    return summary
