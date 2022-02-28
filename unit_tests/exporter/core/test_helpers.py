from exporter.core.helpers import has_valid_rfd_certificate


def test_has_valid_rfd_certificate_is_expired():
    actual = has_valid_rfd_certificate(
        {"organisation": {"documents": [{"document_type": "rfd-certificate", "is_expired": True}]}}
    )

    assert actual is False


def test_has_valid_rfd_certificate_not_expired():
    actual = has_valid_rfd_certificate(
        {"organisation": {"documents": [{"document_type": "rfd-certificate", "is_expired": False}]}}
    )

    assert actual is True


def test_has_valid_rfd_certificate_empty():
    actual = has_valid_rfd_certificate({"organisation": {"documents": []}})

    assert actual is False
