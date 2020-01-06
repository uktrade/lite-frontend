from django.template.defaultfilters import default

from goods.services import post_good_documents
from lite_forms.components import Summary


def good_summary(good):
    if not good:
        return

    return Summary(
        values={
            "Description": good["description"],
            "Control list entry": default(good["control_code"], "N/A"),
            "Part number": default(good["part_number"], "N/A"),
        },
        classes=["govuk-summary-list--no-border"],
    )


def good_document_upload(request, good_id, data):
    if "description" not in data:
        data["description"] = ""
    data = [data]

    # Send LITE API the file information
    good_documents, _ = post_good_documents(request, good_id, data)
    return good_documents
