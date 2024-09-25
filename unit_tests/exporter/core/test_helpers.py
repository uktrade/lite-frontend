from core.constants import OrganisationDocumentType

from exporter.core.helpers import has_valid_rfd_certificate, convert_control_list_entries_to_options
from lite_forms.components import Option


def test_has_valid_rfd_certificate_is_expired():
    actual = has_valid_rfd_certificate(
        {
            "organisation": {
                "documents": [{"document_type": OrganisationDocumentType.RFD_CERTIFICATE, "is_expired": True}]
            }
        }
    )

    assert actual is False


def test_has_valid_rfd_certificate_not_expired():
    actual = has_valid_rfd_certificate(
        {
            "organisation": {
                "documents": [{"document_type": OrganisationDocumentType.RFD_CERTIFICATE, "is_expired": False}]
            }
        }
    )

    assert actual is True


def test_has_valid_rfd_certificate_empty():
    actual = has_valid_rfd_certificate({"organisation": {"documents": []}})

    assert actual is False


def test_convert_control_list_entries_to_options(data_control_list_entries):
    converted_control_list_entries = convert_control_list_entries_to_options(data_control_list_entries)

    for index, option in enumerate(converted_control_list_entries):
        assert type(option) == Option
        assert option.key == data_control_list_entries[index]["rating"]
        assert option.value == data_control_list_entries[index]["rating"]
        assert option.description == data_control_list_entries[index]["text"]
