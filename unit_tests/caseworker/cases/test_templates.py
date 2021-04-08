import requests
from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from caseworker.cases.objects import Case


team1 = {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "team1", "part_of_ecju": None}
team2 = {"id": "47762273-5655-4ce3-afa1-b34112f3e781", "name": "team2", "part_of_ecju": None}

john_smith = {
    "email": "john.smith@example.com",
    "first_name": "John",
    "id": "63c74ddd-c119-48cc-8696-d196218ca583",
    "last_name": "Smith",
    "role_name": "Super User",
    "status": "Active",
    "team": team1,
}
jane_doe = {
    "email": "jane.doe@example.com",
    "first_name": "Jane",
    "id": "24afb1dc-fa1e-40d1-a716-840585c85ebc",
    "last_name": "Doe",
    "role_name": "Super User",
    "status": "Active",
    "team": team2,
}


def test_no_user_advice_checkboxes_visible_no_combine_button(data_standard_case):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user"]
    html = render_to_string("case/tabs/user-advice.html", context)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-combine-user-advice").parent["class"]
    assert soup.find(id="link-select-all-goods")
    assert soup.find(id="link-select-all-destinations")


def test_no_user_advice_checkboxes_visible_no_combine_button_grouped_view(data_standard_case, rf, client):
    context = {}
    context["queue"] = {"id": "00000000-0000-0000-0000-000000000001"}
    case = {**data_standard_case}
    context["case"] = Case(case["case"])
    context["current_user"] = jane_doe
    context["current_advice_level"] = ["user"]
    case_id = context["case"].id
    queue_id = context["queue"].id

    request = rf.get(f"/queues/{queue_id}/cases/{case_id}/user-advice/?grouped-advice-view=True")
    request.session = client.session
    request.requests_session = requests.Session()

    html = render_to_string("case/tabs/user-advice.html", context=context, request=request)
    soup = BeautifulSoup(html, "html.parser")
    assert "app-advice__disabled-buttons" in soup.find(id="button-combine-user-advice").parent["class"]
    assert soup.find(id="button-select-all-no_advice")
