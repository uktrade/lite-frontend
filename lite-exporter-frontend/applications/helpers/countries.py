from enum import Enum

from lite_content.lite_exporter_frontend.applications import ContractTypes as contractTypeStrings


class ContractTypes(Enum):
    NUCLEAR_RELATED = "nuclear_related"
    NAVY = "navy"
    ARMY = "army"
    AIR_FORCE = "air_force"
    POLICE = "police"
    MINISTRY_OF_INTERIOR = "ministry_of_interior"
    OTHER_SECURITY_FORCES = "other_security_forces"
    COMPANIES_NUCLEAR_RELATED = "companies_nuclear_related"
    MARITIME_ANTI_PIRACY = "maritime_anti_piracy"
    AIRCRAFT_MANUFACTURERS = "aircraft_manufacturers"
    REGISTERED_FIREARM_DEALERS = "registered_firearm_dealers"
    OIL_AND_GAS_INDUSTRY = "oil_and_gas_industry"
    PHARMACEUTICAL_OR_MEDICAL = "pharmaceutical_or_medical"
    MEDIA = "media"
    PRIVATE_MILITARY = "private_military"
    EDUCATION = "education"
    FOR_THE_EXPORTERS_OWN_USE = "for_the_exporters_own_use"
    OTHER_CONTRACT_TYPE = "other_contract_type"

    @classmethod
    def string_mapping(cls):
        return {
            ContractTypes.NUCLEAR_RELATED: contractTypeStrings.NUCLEAR_RELATED,
            ContractTypes.NAVY: contractTypeStrings.NAVY,
            ContractTypes.ARMY: contractTypeStrings.ARMY,
            ContractTypes.AIR_FORCE: contractTypeStrings.AIR_FORCE,
            ContractTypes.POLICE: contractTypeStrings.POLICE,
            ContractTypes.MINISTRY_OF_INTERIOR: contractTypeStrings.MINISTRY_OF_INTERIOR,
            ContractTypes.OTHER_SECURITY_FORCES: contractTypeStrings.OTHER_SECURITY_FORCES,
            ContractTypes.COMPANIES_NUCLEAR_RELATED: contractTypeStrings.COMPANIES_NUCLEAR_RELATED,
            ContractTypes.MARITIME_ANTI_PIRACY: contractTypeStrings.MARITIME_ANTI_PIRACY,
            ContractTypes.AIRCRAFT_MANUFACTURERS: contractTypeStrings.AIRCRAFT_MANUFACTURERS,
            ContractTypes.REGISTERED_FIREARM_DEALERS: contractTypeStrings.REGISTERED_FIREARM_DEALERS,
            ContractTypes.OIL_AND_GAS_INDUSTRY: contractTypeStrings.OIL_AND_GAS_INDUSTRY,
            ContractTypes.PHARMACEUTICAL_OR_MEDICAL: contractTypeStrings.PHARMACEUTICAL_OR_MEDICAL,
            ContractTypes.MEDIA: contractTypeStrings.MEDIA,
            ContractTypes.PRIVATE_MILITARY: contractTypeStrings.PRIVATE_MILITARY,
            ContractTypes.EDUCATION: contractTypeStrings.EDUCATION,
            ContractTypes.FOR_THE_EXPORTERS_OWN_USE: contractTypeStrings.FOR_THE_EXPORTERS_OWN_USE,
            ContractTypes.OTHER_CONTRACT_TYPE: contractTypeStrings.OTHER,
        }

    @classmethod
    def get_str_representation(cls, key):
        return ContractTypes.string_mapping()[key]


def prettify_country_data(countries):
    for country in countries:
        pretty_contract_types = []
        if country["contract_types"]:
            contract_types = country["contract_types"].split(",")
            for contract_type in contract_types:
                if contract_type != "other_contract_type":
                    pretty_contract_types.append(ContractTypes.get_str_representation(ContractTypes(contract_type)))
            country["contract_types"] = pretty_contract_types
    return countries
