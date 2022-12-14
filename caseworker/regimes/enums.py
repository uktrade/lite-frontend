from enum import Enum


class Regimes(str, Enum):
    WASSENAAR = "WASSENAAR"
    MTCR = "MTCR"
    NSG = "NSG"
    CWC = "CWC"
    AG = "AG"
