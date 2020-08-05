from enum import Enum


class F680:
    FIELDS = [
        "expedited",
        "expedited_date",
        "expedited_description",
        "foreign_technology",
        "foreign_technology_description",
        "locally_manufactured",
        "locally_manufactured_description",
        "mtcr_type",
        "electronic_warfare_requirement",
        "uk_service_equipment",
        "uk_service_equipment_description",
        "uk_service_equipment_type",
        "prospect_value",
    ]
    REQUIRED_FIELDS = [
        "expedited",
        "foreign_technology",
        "locally_manufactured",
        "mtcr_type",
        "electronic_warfare_requirement",
        "uk_service_equipment",
        "prospect_value",
    ]

    REQUIRED_SECONDARY_FIELDS = {
        "foreign_technology": "foreign_technology_description",
        "expedited": "expedited_date",
        "locally_manufactured": "locally_manufactured_description",
    }


class OielLicenceTypes(Enum):
    MEDIA = "media"
    CRYPTOGRAPHIC = "cryptographic"
    DEALER = "dealer"
    UK_CONTINENTAL_SHELF = "uk_continental_shelf"

    @classmethod
    def is_non_editable_good(cls, value):
        return value in [
            OielLicenceTypes.MEDIA.value,
            OielLicenceTypes.CRYPTOGRAPHIC.value,
            OielLicenceTypes.DEALER.value,
        ]

    @classmethod
    def is_non_editable_country(cls, value):
        return value in [
            OielLicenceTypes.MEDIA.value,
            OielLicenceTypes.CRYPTOGRAPHIC.value,
            OielLicenceTypes.DEALER.value,
            OielLicenceTypes.UK_CONTINENTAL_SHELF.value,
        ]
