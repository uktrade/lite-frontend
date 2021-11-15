import pytest
from django.urls import reverse

from exporter.applications.forms import locations as locations_forms

APPLICATION_ID = "8fb76bed-fd45-4293-95b8-eda9468aa254"


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
    "url,valid_data,success_url",
    [
        (
            reverse("applications:edit_location", kwargs={"pk": APPLICATION_ID}),
            {"goods_starting_point": "GB"},
            reverse("applications:temporary_or_permanent", kwargs={"pk": APPLICATION_ID}),
        ),
        (
            reverse("applications:temporary_or_permanent", kwargs={"pk": APPLICATION_ID}),
            {"export_type": "temporary"},
            reverse("applications:temporary_export_details", kwargs={"pk": APPLICATION_ID}),
        ),
        (
            reverse("applications:temporary_or_permanent", kwargs={"pk": APPLICATION_ID}),
            {"export_type": "permanent"},
            reverse("applications:route_of_goods", kwargs={"pk": APPLICATION_ID}),
        ),
        (
            reverse("applications:route_of_goods", kwargs={"pk": APPLICATION_ID}),
            {"is_shipped_waybill_or_lading": True},
            reverse("applications:goods_recipients", kwargs={"pk": APPLICATION_ID}),
        ),
        (
            reverse("applications:goods_recipients", kwargs={"pk": APPLICATION_ID}),
            {"goods_recipients": "direct_to_end_user"},
            reverse("applications:locations_summary", kwargs={"pk": APPLICATION_ID}),
        ),
    ],
)
def test_form_view_redirects(
    url,
    valid_data,
    success_url,
    authorized_client,
    data_standard_case,
    mock_get_application,
    mock_put_application,
    mock_put_application_route_of_goods,
):
    response = authorized_client.post(url, data=valid_data)
    assert response.status_code == 302
    assert response.url == success_url
