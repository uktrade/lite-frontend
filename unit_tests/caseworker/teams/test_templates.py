from bs4 import BeautifulSoup
import re

from django.template.loader import render_to_string


def test_pending_users_in_team_members(john_smith, gov_uk_user_id):
    context = {}
    context["users"] = [
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
        },
        john_smith,
    ]
    html = render_to_string("teams/team.html", context)
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all(id=re.compile("^row-\d+"))
    assert rows[0].find(class_="govuk-tag govuk-tag--blue").text.strip() == "Pending"
    assert rows[1].find(class_="govuk-table__header").text.strip() == "John Smith"

    values_for_assert = ["john.smith@example.com", "Active", "View"]
    for index, value in enumerate(rows[1].find_all(class_="govuk-table__cell")):
        assert values_for_assert[index] == value.text.strip()
