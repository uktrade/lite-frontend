from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.applications.forms import parties


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"reuse_party": "True"}, True, None),
        ({"reuse_party": ""}, False, {"reuse_party": ["Select yes if you want to reuse an existing party"]}),
    ),
)
def test_party_reuse_form(data, valid, errors):
    form = parties.PartyReuseForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"sub_type": "government"}, True, None),
        ({"sub_type": "other", "sub_type_other": "test_sub_type"}, True, None),
        ({"sub_type": ""}, False, {"sub_type": ["Select what type of party you're creating"]}),
        ({"sub_type": "other"}, False, {"sub_type_other": ["Enter the type of the party you're adding"]}),
    ),
)
def test_party_subtype_select_form(data, valid, errors):
    form = parties.PartySubTypeSelectForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"name": "test"}, True, None),
        ({"name": ""}, False, {"name": ["Enter a name"]}),
    ),
)
def test_party_name_form(data, valid, errors):
    form = parties.PartyNameForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"website": "test"}, True, None),
        ({"website": ""}, True, None),
        ({}, True, None),
    ),
)
def test_party_website_form(data, valid, errors):
    form = parties.PartyWebsiteForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"address": "1 somewhere", "country": "aus"}, True, None),
        ({"address": "", "country": ""}, False, {"address": ["Enter an address"], "country": ["Select the country"]}),
    ),
)
@patch("exporter.applications.forms.parties.get_countries")
def test_party_address_form(mock_get_countries, data, valid, errors):
    class Request:
        csp_nonce = "test"

    request = Request()
    mock_get_countries.return_value = [{"id": "aus", "name": "Austria"}, {"id": "fr", "name": "France"}]
    form = parties.PartyAddressForm(request=request, data=data)

    assert form.is_valid() == valid
    mock_get_countries.assert_called_once_with(request)

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"signatory_name_euu": "test"}, True, None),
        ({"signatory_name_euu": ""}, False, {"signatory_name_euu": ["Enter a name"]}),
    ),
)
def test_party_signatory_name_form(data, valid, errors):
    form = parties.PartySignatoryNameForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"end_user_document_available": "True"}, True, None),
        (
            {"end_user_document_available": ""},
            False,
            {"end_user_document_available": ["Select yes if you have an end-user document"]},
        ),
        ({"end_user_document_available": "False", "end_user_document_missing_reason": "test reason"}, True, None),
        (
            {"end_user_document_available": "False", "end_user_document_missing_reason": ""},
            False,
            {
                "end_user_document_missing_reason": [
                    "Enter why you do not have an end-user undertaking or stockist undertaking"
                ]
            },
        ),
    ),
)
def test_party_documents_form(data, valid, errors):
    form = parties.PartyDocumentsForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, edit, valid, errors",
    (
        (
            {"description": "test", "document_in_english": "True", "document_on_letterhead": "True"},
            {"party_document": SimpleUploadedFile("test", b"test_content")},
            False,
            True,
            None,
        ),
        (
            {"description": "test", "document_in_english": "True", "document_on_letterhead": "True"},
            {},
            True,
            True,
            None,
        ),
        (
            {"description": "", "document_in_english": "", "document_on_letterhead": ""},
            {},
            False,
            False,
            {
                "party_document": ["Select an end-user document"],
                "document_in_english": ["Select yes if the end-user document is in English"],
                "document_on_letterhead": [
                    "Select yes if the document includes at least one page on company letterhead"
                ],
            },
        ),
        (
            {"description": "", "document_in_english": "", "document_on_letterhead": ""},
            {},
            False,
            False,
            {
                "party_document": ["Select an end-user document"],
                "document_in_english": ["Select yes if the end-user document is in English"],
                "document_on_letterhead": [
                    "Select yes if the document includes at least one page on company letterhead"
                ],
            },
        ),
    ),
)
def test_party_document_upload_form(data, files, edit, valid, errors):
    form = parties.PartyDocumentUploadForm(edit=edit, data=data, files=files)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, edit, valid, errors",
    (
        (
            {},
            {"party_eng_translation_document": SimpleUploadedFile("test", b"test_content")},
            False,
            True,
            None,
        ),
        (
            {},
            {},
            True,
            True,
            None,
        ),
        (
            {},
            {},
            False,
            False,
            {
                "party_eng_translation_document": ["Select an English translation"],
            },
        ),
    ),
)
def test_party_english_translation_document_upload_form(data, files, edit, valid, errors):
    form = parties.PartyEnglishTranslationDocumentUploadForm(edit=edit, data=data, files=files)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, edit, valid, errors",
    (
        (
            {},
            {"party_letterhead_document": SimpleUploadedFile("test", b"test_content")},
            False,
            True,
            None,
        ),
        (
            {},
            {},
            True,
            True,
            None,
        ),
        (
            {},
            {},
            False,
            False,
            {
                "party_letterhead_document": ["Select a document on company letterhead"],
            },
        ),
    ),
)
def test_party_company_letterhead_document_upload_form(data, files, edit, valid, errors):
    form = parties.PartyCompanyLetterheadDocumentUploadForm(edit=edit, data=data, files=files)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors
