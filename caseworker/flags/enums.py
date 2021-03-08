from enum import Enum

from caseworker.core.constants import Permission


class FlagLevel:
    CASES = "Cases"
    ORGANISATIONS = "Organisations"
    GOODS = "Goods"
    DESTINATIONS = "Destinations"


class FlagStatus(Enum):
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"


class FlagPermissions:
    DEFAULT = "Anyone"
    AUTHORISED_COUNTERSIGNER = "Authorised countersigner"
    HEAD_OF_LICENSING_UNIT_COUNTERSIGNER = "Head of Licensing Unit countersigner"

    PERMISSIONS_MAPPING = {
        AUTHORISED_COUNTERSIGNER: Permission.REMOVE_AUTHORISED_COUNTERSINGER_FLAGS,
        HEAD_OF_LICENSING_UNIT_COUNTERSIGNER: Permission.REMOVE_HEAD_OF_LICENSING_UNIT_FLAGS,
    }
