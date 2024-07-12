from django.conf import settings

SERVICE_NAME = "LITE"

BACK = "Back"
BACK_TO_APPLICATION_OVERVIEW = "Back to application overview"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"
SAVE_AND_RETURN = "Save and return to application overview"
VIEW = "View"
CHANGE = "Change"
CONFIRM_AND_CONTINUE = "Confirm and continue"

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
PERMISSION_FINDER_LINK = "[control list](" + settings.PERMISSIONS_FINDER_URL + ")"


class Filters:
    SHOW_FILTERS_LINK = "Show filters"
    HIDE_FILTERS_LINK = "Hide filters"
    APPLY_FILTERS_BUTTON = "Apply filters"
    CLEAR_FILTERS_BUTTON = "Clear filters"
    FILTER_BY_PREFIX = "Filter by"


class Checkboxes:
    SELECT_DESELECT_ALL = "Select all/Deselect all"


class Address:
    ADDRESS = "Address"
    ADDRESS_LINE_1 = "Building and street"
    ADDRESS_LINE_2 = ""
    TOWN = "Town or city"
    COUNTY = "County or state"
    POSTAL_CODE = "Postcode"
    COUNTRY = "Country"
