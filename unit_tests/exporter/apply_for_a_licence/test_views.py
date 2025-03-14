import pytest

from django.http import HttpResponse
from django.urls import reverse


@pytest.fixture()
def licence_type_url():
    return reverse("apply_for_a_licence:start")


@pytest.mark.parametrize(
    "licence_type, processor_class",
    (
        ("export_licence", "ExportLicenceLicenceTypeProcessor"),
        ("f680", "F680LicenceLicenceTypeProcessor"),
    ),
)
def test_licence_type_delegates_to_processor(
    authorized_client,
    licence_type_url,
    licence_type,
    processor_class,
    mocker,
    settings,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True

    mock_process_class = mocker.patch(f"exporter.apply_for_a_licence.views.{processor_class}")
    mock_process_object = mock_process_class()

    returned_response = HttpResponse("OK")
    mock_process_object.process.return_value = returned_response

    response = authorized_client.post(
        licence_type_url,
        data={"licence_type": licence_type},
    )

    mock_process_class.assert_called_with(response.wsgi_request)

    mock_process_object.process.assert_called()
    assert response == returned_response
