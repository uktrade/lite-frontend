import pytest

from django.core.exceptions import ValidationError

from exporter.core.organisation.validators import validate_phone, validate_registration, validate_website


@pytest.mark.parametrize(
    "phone_number",
    (
        "+44 1234 567921",
        "+44-1234-567921",
        "+44-7977-567921",
        "+33 5 97 75 67 92",
        "01234 567921",
        "(01234) 567921",
        "(01234) - 567921",
        "01234567921",
        "(07777)567921",
    ),
)
def test_validate_phone_valid_numbers(phone_number):
    assert validate_phone(phone_number) is None


@pytest.mark.parametrize(
    "phone_number",
    (
        "9234 567921",
        "(9234) 567921",
        "67921",
        "banana",
        "01234@567921",
    ),
)
def test_validate_phone_number_invalid_numbers(phone_number):
    with pytest.raises(ValidationError):
        validate_phone(phone_number)


@pytest.mark.parametrize(
    "registration_number",
    ("12345678", "RA123456", "ra123456", "01235233"),
)
def test_validate_registration_number_valid_numbers(registration_number):
    assert validate_registration(registration_number) is registration_number


@pytest.mark.parametrize(
    "registration_number",
    ("9234567921", "TAF12345", "BJLALKWD", " "),
)
def test_validate_registration_number_invalid_numbers(registration_number):
    with pytest.raises(ValidationError):
        validate_registration(registration_number)


@pytest.mark.parametrize(("website"), ["https://www.example.com", "www.example.com", "example.com", ""])
def test_validate_website(website):
    assert validate_website(website) is website


@pytest.mark.parametrize(("website"), ["example", "com", ".com"])
def test_validate_website_invalid_url(website):
    with pytest.raises(ValidationError):
        validate_website(website)
