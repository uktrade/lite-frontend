from conf.settings import env

SERVICE_NAME = "LITE"

BACK = "Back"
BACK_TO_APPLICATION_OVERVIEW = "Back to application overview"

DESCRIPTION = "Description"
PART_NUMBER = "Part number"
CONTROLLED = "Controlled"
INCORPORATED = "Incorporated"


class NoticeComponent:
    INFORMATION = "Information"


class Document:
    DOWNLOAD = "Download"
    DELETE = "Delete"
    PROCESSING = "Processing"
    ATTACH = "Attach"
    REMOVE = "Remove"
    ACCESS_DENIED = "You don't have access to this document"


# Links
PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"
