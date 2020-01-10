from conf.settings import env

SERVICE_NAME = "LITE"

BACK = "Back"
BACK_TO_APPLICATION_OVERVIEW = "Back to application overview"

DESCRIPTION = "Description"
PART_NUMBER = "Part number"
CONTROL_LIST_ENTRY = "Control list entry"
CONTROLLED = "Controlled"
INCORPORATED = "Incorporated"
INFORMATION = "Information"


class Document:
    DOWNLOAD = "Download"
    DELETE = "Delete"
    PROCESSING = "Processing"
    ATTACH = "Attach"
    REMOVE = "Remove"


# Links
PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"
