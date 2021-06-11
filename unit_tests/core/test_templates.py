import pytest
from bs4 import BeautifulSoup
from django.template.loader import render_to_string


@pytest.mark.parametrize(
    "allow_clc_query_pv_grading", [(True), (False),],
)
def test_clc_query_and_pv_grading_application_links(allow_clc_query_pv_grading):
    context = {
        "organisation": {},
        "user_data": {},
        "notifications": [],
        "existing": False,
        "user_permissions": [],
        "FEATURE_FLAG_ONLY_ALLOW_SIEL": True,
        "FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING": allow_clc_query_pv_grading,
    }

    html = render_to_string("core/hub.html", context)
    soup = BeautifulSoup(html, "html.parser")
    clc_query_link = soup.find(id="clc_query_link_value")
    pv_grading_link = soup.find(id="pv_grading_link_value")
    if allow_clc_query_pv_grading:
        clc_query_link = clc_query_link.text.strip("\n\t")
        pv_grading_link = pv_grading_link.text.strip("\n\t")
        assert clc_query_link == "Create a control list classification (CLC) query"
        assert pv_grading_link == "Apply for a security grading"
    else:
        assert clc_query_link == None
        assert pv_grading_link == None
