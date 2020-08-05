from enum import Enum


class FlagLevel:
    CASES = "Cases"
    ORGANISATIONS = "Organisations"
    GOODS = "Goods"
    DESTINATIONS = "Destinations"


class FlagStatus(Enum):
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"
