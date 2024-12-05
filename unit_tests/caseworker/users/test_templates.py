from bs4 import BeautifulSoup
import re

from django.template.loader import render_to_string

from caseworker.core.constants import SUPER_USER_ROLE_ID


def test_pending_users_in_all_users(john_smith, gov_uk_user_id, get_mock_request_user, mock_gov_user):
    context = {}
    context["data"] = {
        "results": [
            {
                "id": gov_uk_user_id,
                "email": "jane.doe@example.com",
                "first_name": "",
                "last_name": "",
                "status": "Active",
                "team": {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "name": "Admin",
                    "alias": None,
                    "part_of_ecju": None,
                    "is_ogd": False,
                },
                "role_name": "Super User",
                "pending": True,
                "role": {"id": SUPER_USER_ROLE_ID},
            },
            john_smith,
        ]
    }

    request = get_mock_request_user(mock_gov_user["user"])
    html = render_to_string(template_name="users/index.html", context=context, request=request)
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all(id=re.compile("^row-\d+"))
    assert rows[0].find(class_="govuk-tag govuk-tag--blue").text.strip() == "Pending"
    assert rows[1].find(class_="govuk-table__header").text.strip() == "John Smith"

    values_for_assert = ["john.smith@example.com", "A team", "Super User", "Active", "View"]
    for index, value in enumerate(rows[1].find_all(class_="govuk-table__cell")):
        assert values_for_assert[index] == value.text.strip()
