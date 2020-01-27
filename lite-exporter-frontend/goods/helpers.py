from django.template.defaultfilters import default

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


def process_pv_grading_for_post(json):
    post_data = json
    # Convert date
    date_field = "date_of_issue"
    year = json.get(date_field + "year", "")
    month = json.get(date_field + "month", "")
    if len(month) == 1:
        month = "0" + month
    day = json.get(date_field + "day", "")
    if len(day) == 1:
        day = "0" + day
    date_of_issue = f"{year}-{month}-{day}"

    post_data["pv_grading_details"] = {
        "grading": post_data["grading"],
        "custom_grading": post_data["custom_grading"],
        "prefix": post_data["prefix"],
        "suffix": post_data["suffix"],
        "issuing_authority": post_data["issuing_authority"],
        "reference": post_data["reference"],
        "date_of_issue": date_of_issue,
    }

    return post_data
