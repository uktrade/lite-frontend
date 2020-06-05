from typing import Dict


def get_matching_flags(items: Dict):
    """
    Returns none if mismatched, else returns the flags
    """
    if items:
        flags = items[0]["flags"]

        for item in items:
            for flag in item["flags"]:
                if flag not in flags:
                    return

        return flags
