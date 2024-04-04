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
        "exceptional_circumstances",
        "foreign_technology_information",
        "is_local_assembly_manufacture",
        "product_mtcr_rating_type",
        "ew_data",
        "armed_forces_usage",
    ]

    REQUIRED_SECONDARY_FIELDS = {
        "foreign_technology_information": "foreign_technology_information_details",
        "is_local_assembly_manufacture": "is_local_assembly_manufacture_details",
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
