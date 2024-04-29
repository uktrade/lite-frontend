from enum import Enum


class F680:
    FIELDS = [
        "exceptional_circumstances",
        "foreign_technology_information",
        "foreign_technology_information_details",
        "is_local_assembly_manufacture",
        "is_local_assembly_manufacture_details",
        "product_mtcr_rating_type",
        "product_mtcr_rating_type_details",
        "ew_data",
        "product_funding",
        "armed_forces_usage",
        "armed_forces_usage_details",
    ]
    REQUIRED_FIELDS = [
        "exceptional_circumstances",
        "foreign_technology_information",
        "is_local_assembly_manufacture",
        "product_mtcr_rating_type",
        "ew_data",
        "armed_forces_usage",
        "product_funding",
    ]

    REQUIRED_SECONDARY_FIELDS = {
        "foreign_technology_information": "foreign_technology_information_details",
        "is_local_assembly_manufacture": "is_local_assembly_manufacture_details",
        "product_mtcr_rating_type": "product_mtcr_rating_type_details",
        "armed_forces_usage": "armed_forces_usage_details",
    }


class OIEL:
    FIELDS = [
        "exceptional_circumstances",
        "foreign_technology_information",
        "foreign_technology_information_details",
        "is_local_assembly_manufacture",
        "is_local_assembly_manufacture_details",
        "product_mtcr_rating_type",
        "product_mtcr_rating_type_details",
        "ew_data",
        "product_funding",
        "armed_forces_usage",
        "armed_forces_usage_details",
    ]
    REQUIRED_FIELDS = [
        "exceptional_circumstances",
        "foreign_technology_information",
        "is_local_assembly_manufacture",
        "product_mtcr_rating_type",
        "ew_data",
        "armed_forces_usage",
        "product_funding",
    ]

    REQUIRED_SECONDARY_FIELDS = {
        "foreign_technology_information": "foreign_technology_information_details",
        "is_local_assembly_manufacture": "is_local_assembly_manufacture_details",
        "product_mtcr_rating_type": "product_mtcr_rating_type_details",
        "armed_forces_usage": "armed_forces_usage_details",
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
