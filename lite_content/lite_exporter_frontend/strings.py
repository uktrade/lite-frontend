from conf.settings import env
from lite_content.lite_exporter_frontend import (  # noqa
    applications,  # noqa
    goods,  # noqa
    roles,  # noqa
    users,  # noqa
    sites,  # noqa
    core,  # noqa
    end_users,  # noqa
    hub,  # noqa
    third_parties,  # noqa
    generic,  # noqa
)  # noqa

# Generic (used as defaults in forms)
BACK_TO_APPLICATION = "Back to application"
YES = "Yes"
NO = "No"
SUBMIT = "Submit"
SAVE = "Save"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"
CANCEL = "Cancel"
POST_NOTE = "Post note"
THERE_IS_A_PROBLEM = "There is a problem"

THIS_SECTION_IS = "This section is "  # The space at the end is intentional. Usage is 'This section is optional'
OPTIONAL = "Optional"
NOT_STARTED = "Not started"
IN_PROGRESS = "In progress"
DONE = "Completed"
VIEW = "View"

SUBMIT_APPLICATION = "Submit application"
EDIT_APPLICATION_SUBMIT = "Submit application"
EDIT_APPLICATION_DONE = "Completed"

HOME = "Home"

# Constants
PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"


class Address:
    ADDRESS_LINE_1 = "Building and street"
    ADDRESS_LINE_2 = ""
    TOWN = "Town or city"
    COUNTY = "County or state"
    POSTAL_CODE = "Postcode"
    COUNTRY = "Country"
