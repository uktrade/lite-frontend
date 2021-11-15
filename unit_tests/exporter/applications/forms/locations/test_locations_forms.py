import pytest
from django.urls import reverse

from exporter.applications.forms import locations as locations_forms


@pytest.mark.parametrize(
    "form_class,data,is_valid",
    [
        (locations_forms.GoodsStartingPointForm, {"goods_starting_point": "GB"}, True),
        (locations_forms.GoodsStartingPointForm, {"goods_starting_point": "NI"}, True),
        (locations_forms.GoodsStartingPointForm, {"goods_starting_point": ""}, False),
        (locations_forms.GoodsStartingPointForm, {"goods_starting_point": None}, False),
        (locations_forms.PermanentOrTemporaryExportForm, {"export_type": "permanent"}, True),
        (locations_forms.PermanentOrTemporaryExportForm, {"export_type": "temporary"}, True),
        (locations_forms.PermanentOrTemporaryExportForm, {"export_type": ""}, False),
        (locations_forms.PermanentOrTemporaryExportForm, {"export_type": None}, False),
        (locations_forms.GoodsRecipientsForm, {"goods_recipients": "direct_to_end_user"}, True),
        (locations_forms.GoodsRecipientsForm, {"goods_recipients": "via_consignee"}, True),
        (locations_forms.GoodsRecipientsForm, {"goods_recipients": "via_consignee_and_third_parties"}, True),
        (locations_forms.GoodsRecipientsForm, {"goods_recipients": ""}, False),
        (locations_forms.GoodsRecipientsForm, {"goods_recipients": None}, False),
    ],
)
def test_locations_forms_validation(form_class, data, is_valid):
    form = form_class(data=data)
    if is_valid:
        assert form.is_valid()
        assert form.cleaned_data == data
    else:
        assert not form.is_valid()


@pytest.mark.parametrize(
    "url_name,valid_data,success_url_name",
    [
        (
            "applications:edit_location",
            {"goods_starting_point": "GB"},
            "applications:temporary_or_permanent",
        ),
        (
            "applications:temporary_or_permanent",
            {"export_type": "temporary"},
            "applications:temporary_export_details",
        ),
        (
            "applications:temporary_or_permanent",
            {"export_type": "permanent"},
            "applications:route_of_goods",
        ),
        (
            "applications:route_of_goods",
            {"is_shipped_waybill_or_lading": True},
            "applications:goods_recipients",
        ),
        (
            "applications:goods_recipients",
            {"goods_recipients": "direct_to_end_user"},
            "applications:locations_summary",
        ),
    ],
)
def test_form_view_redirects(
    url_name,
    valid_data,
    success_url_name,
    authorized_client,
    data_standard_case,
    mock_get_application,
    mock_put_application,
    mock_put_application_route_of_goods,
):
    response = authorized_client.post(reverse(url_name, kwargs={"pk": data_standard_case["case"]["id"]}), data=valid_data)
    assert response.status_code == 302
    assert response.url == reverse(success_url_name, kwargs={"pk": data_standard_case["case"]["id"]})
