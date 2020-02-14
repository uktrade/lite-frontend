from conf.settings import env

SERVICE_NAME = "LITE"

BACK = "Back"
BACK_TO_APPLICATION_OVERVIEW = "Back to application overview"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"
SAVE_AND_RETURN = "Save and return to task list"

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
    DOWNLOAD_ERROR = "This document cannot be downloaded at the moment"


# Links
PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"
