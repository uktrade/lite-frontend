from enum import Enum


class ServiceType(Enum):
    CASEWORKER = "CASEWORKER"
    EXPORTER = "EXPORTER"


class ManifestType(Enum):
    CASEWORKER_STANDARD_APPLICATION = "CASEWORKER_application"
    EXPORTER_STANDARD_APPLICATION = "EXPORTER_application"

    CASEWORKER_F680 = "CASEWORKER_security_clearance"
    EXPORTER_F680 = "EXPORTER_security_clearance"
