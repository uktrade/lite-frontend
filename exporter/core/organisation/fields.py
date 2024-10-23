from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from .constants import Validation


class AddressLineField(forms.CharField):
    default_validators = [
        MaxLengthValidator(Validation.ADDRESS_LINE_MAX_LENGTH, Validation.ADDRESS_LINE_MAX_LENGTH_ERROR_MESSAGE)
    ]


class VatField(forms.CharField):
    default_validators = [
        MinLengthValidator(Validation.UK_VAT_MIN_LENGTH, Validation.UK_VAT_MIN_LENGTH_ERROR_MESSAGE),
        MaxLengthValidator(Validation.UK_VAT_MAX_LENGTH, Validation.UK_VAT_MAX_LENGTH_ERROR_MESSAGE),
        RegexValidator(Validation.LETTERS_AND_NUMBERS_ONLY, Validation.UK_VAT_LETTERS_AND_NUMBERS_ERROR_MESSAGE),
        RegexValidator(Validation.UK_VAT_VALIDATION_REGEX, Validation.UK_VAT_VALIDATION_ERROR_MESSAGE),
    ]


class EoriField(forms.CharField):
    default_validators = [
        MinLengthValidator(Validation.UK_EORI_MIN_LENGTH, Validation.UK_EORI_MIN_LENGTH_ERROR_MESSAGE),
        MaxLengthValidator(Validation.UK_EORI_MAX_LENGTH, Validation.UK_EORI_MAX_LENGTH_ERROR_MESSAGE),
        RegexValidator(Validation.LETTERS_AND_NUMBERS_ONLY, Validation.UK_EORI_LETTERS_AND_NUMBERS_ERROR_MESSAGE),
        RegexValidator(Validation.UK_EORI_STARTING_LETTERS_REGEX, Validation.UK_EORI_STARTING_LETTERS_ERROR_MESSAGE),
        RegexValidator(Validation.UK_EORI_VALIDATION_REGEX, Validation.UK_EORI_VALIDATION_ERROR_MESSAGE),
    ]


class SicField(forms.CharField):
    default_validators = [
        MinLengthValidator(Validation.SIC_LENGTH, Validation.SIC_NUMBER_LENGTH_ERROR_MESSAGE),
        MaxLengthValidator(Validation.SIC_LENGTH, Validation.SIC_NUMBER_LENGTH_ERROR_MESSAGE),
        RegexValidator(Validation.SIC_NUMBERs_ONLY_REGEX, Validation.SIC_NUMBERS_ONLY_ERROR_MESSAGE),
    ]
