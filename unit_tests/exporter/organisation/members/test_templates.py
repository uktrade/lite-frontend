from bs4 import BeautifulSoup

from django.template.loader import render_to_string


def test_pending_users_in_organisation():
    context = {}
    context["data"] = {
        "results": [
            {
                "id": "11c74ddd-c119-48cc-8696-e096218ca583",
                "email": "jane.doe@example.com",
                "first_name": "",
                "last_name": "",
                "status": "Active",
                "role_name": "Super User",
                "pending": True,
                "phone_number": "",
            },
            {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "email": "john.smith@example.com",
                "first_name": "John",
                "last_name": "Smith",
                "status": "Active",
                "role_name": "Administrator",
                "pending": False,
                "phone_number": "",
            },
        ]
    }
    html = render_to_string("organisation/members/index.html", context)
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find("tbody", {"class": "govuk-table__body"}).find_all("tr", recursive=False)
    assert rows[0].find(class_="govuk-tag govuk-tag--blue").text.strip() == "Pending"
    assert rows[1].find(class_="govuk-table__header").text.strip() == "John Smith"

    values_for_assert = ["john.smith@example.com", "Administrator", "Active", "View John Smith's profile"]
    for index, value in enumerate(rows[1].find_all(class_="govuk-table__cell")):
        assert values_for_assert[index] == value.text.strip()
