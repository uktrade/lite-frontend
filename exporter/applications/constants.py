from enum import Enum

CryptoOIELExcludedDestinations = [
    {"id": "AF", "name": "Afghanistan"},
    {"id": "AM", "name": "Armenia"},
    {"id": "AO", "name": "Angola"},
    {"id": "AT", "name": "Austria"},
    {"id": "AU", "name": "Australia"},
    {"id": "AZ", "name": "Azerbaijan"},
    {"id": "BA", "name": "Bosnia and Herzegovina"},
    {"id": "BE", "name": "Belgium"},
    {"id": "BG", "name": "Bulgaria"},
    {"id": "BI", "name": "Burundi"},
    {"id": "CA", "name": "Canada"},
    {"id": "CD", "name": "Congo (Democratic Republic)"},
    {"id": "CH", "name": "Switzerland"},
    {"id": "CN", "name": "China"},
    {"id": "CY", "name": "Cyprus"},
    {"id": "CZ", "name": "Czechia"},
    {"id": "DE", "name": "Germany"},
    {"id": "DK", "name": "Denmark"},
    {"id": "EE", "name": "Estonia"},
    {"id": "ER", "name": "Eritrea"},
    {"id": "ES", "name": "Spain"},
    {"id": "ET", "name": "Ethiopia"},
    {"id": "FI", "name": "Finland"},
    {"id": "FR", "name": "France"},
    {"id": "GR", "name": "Greece"},
    {"id": "HK", "name": "Hong Kong"},
    {"id": "HR", "name": "Croatia"},
    {"id": "HU", "name": "Hungary"},
    {"id": "IE", "name": "Ireland"},
    {"id": "IQ", "name": "Iraq"},
    {"id": "IR", "name": "Iran"},
    {"id": "IT", "name": "Italy"},
    {"id": "JP", "name": "Japan"},
    {"id": "KP", "name": "North Korea"},
    {"id": "LB", "name": "Lebanon"},
    {"id": "LR", "name": "Liberia"},
    {"id": "LT", "name": "Lithuania"},
    {"id": "LU", "name": "Luxembourg"},
    {"id": "LV", "name": "Latvia"},
    {"id": "LY", "name": "Libya"},
    {"id": "MM", "name": "Burma"},
    {"id": "MT", "name": "Malta"},
    {"id": "NG", "name": "Nigeria"},
    {"id": "NL", "name": "Netherlands"},
    {"id": "NO", "name": "Norway"},
    {"id": "NZ", "name": "New Zealand"},
    {"id": "PL", "name": "Poland"},
    {"id": "PT", "name": "Portugal"},
    {"id": "RO", "name": "Romania"},
    {"id": "RU", "name": "Russia"},
    {"id": "RW", "name": "Rwanda"},
    {"id": "SD", "name": "Sudan"},
    {"id": "SE", "name": "Sweden"},
    {"id": "SI", "name": "Slovenia"},
    {"id": "SK", "name": "Slovakia"},
    {"id": "SL", "name": "Sierra Leone"},
    {"id": "SO", "name": "Somalia"},
    {"id": "SS", "name": "South Sudan"},
    {"id": "SY", "name": "Syria"},
    {"id": "TZ", "name": "Tanzania"},
    {"id": "UG", "name": "Uganda"},
    {"id": "US", "name": "United States"},
    {"id": "VE", "name": "Venezuela"},
    {"id": "ZW", "name": "Zimbabwe"},
]


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
        "nature_of_products",
        "number_of_siels_last_year",
        "siels_issued_last_year",
        "destination_countries",
        "purely_commercial",
    ]
    REQUIRED_FIELDS = ["nature_of_products", "siels_issued_last_year", "purely_commercial"]
    REQUIRED_SECONDARY_FIELDS = {}


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
