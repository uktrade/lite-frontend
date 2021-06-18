import pytest
from bs4 import BeautifulSoup
from django.template.loader import render_to_string


def test_clc_query_and_pv_grading_application_links():
    context = {
        "organisation": {},
        "user_data": {},
        "notifications": [],
        "existing": False,
        "user_permissions": [],
        "FEATURE_FLAG_ONLY_ALLOW_SIEL": True,
    }

    html = render_to_string("core/hub.html", context)
    soup = BeautifulSoup(html, "html.parser")
    product_list_tile = soup.find(id="product-list-tile")
    assert len(product_list_tile.findChildren()) == 4
