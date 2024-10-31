from bs4 import BeautifulSoup

from django.template.loader import render_to_string


def test_pending_users_in_headquarters():
    context = {}
    context["site"] = {
        "id": "e240e0f3-4ff8-4caa-88c9-c5723d1dd1fb",
        "users": [
            {
                "id": "11c74ddd-c119-48cc-8696-e096218ca583",
                "email": "jane.doe@example.com",
                "first_name": "",
                "last_name": "",
                "pending": True,
            },
            {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "email": "john.smith@example.com",
                "first_name": "John",
                "last_name": "Smith",
                "pending": False,
            },
        ],
        "admin_users": [
            {
                "id": "11c74ddd-c119-48cc-8696-e096218ca583",
                "email": "jane_admin.doe@example.com",
                "first_name": "",
                "last_name": "",
                "pending": True,
            },
            {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "email": "john_admin.smith@example.com",
                "first_name": "John Admin",
                "last_name": "Smith",
                "pending": False,
            },
        ],
    }
    html = render_to_string("organisation/sites/site.html", context)
    soup = BeautifulSoup(html, "html.parser")
    admin_rows = soup.find(id="admin-users").find_all("div", recursive=False)

    assert admin_rows[0].find(class_="govuk-tag govuk-tag--blue").text.strip() == "Pending"
    assert admin_rows[1].find(class_="govuk-!-font-weight-bold").text.strip() == "John Admin Smith"
    assert admin_rows[1].find(class_="govuk-summary-list__value").text.strip() == "john_admin.smith@example.com"
    assert admin_rows[1].find(class_="govuk-summary-list__actions").text.strip() == "View John Admin Smith's profile"

    user_rows = soup.find(id="users").find_all("div", recursive=False)

    assert user_rows[0].find(class_="govuk-tag govuk-tag--blue").text.strip() == "Pending"
    assert user_rows[1].find(class_="govuk-!-font-weight-bold").text.strip() == "John Smith"
    assert user_rows[1].find(class_="govuk-summary-list__value").text.strip() == "john.smith@example.com"
    assert user_rows[1].find(class_="govuk-summary-list__actions").text.strip() == "View John Smith's profile"
