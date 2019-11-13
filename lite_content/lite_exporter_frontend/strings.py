from conf.settings import env

# Generic
BACK_TO_APPLICATION = "Back to application"
YES = "Yes"
NO = "No"
SUBMIT = "Submit"
SAVE = "Save"

PERMISSION_FINDER_LINK = (
    '<a class="govuk-link" href="'
    + env("PERMISSIONS_FINDER_URL")
    + '">Permissions Finder</a>'
)

APPLICATION_GOODS_TITLE = "Goods"
APPLICATION_GOODS_ADD_NEW = "Add a new good"
APPLICATION_GOODS_ADD_BACK = "Back to goods"
APPLICATION_GOODS_ADD_APPLICATION_DETAILS = "Details for good on application"
APPLICATION_GOODS_ADD_DOCUMENT_DESCRIPTION = (
    "To finish creating the good, you must attach a document."
    "\n\nWarning: Do not upload any document which is above "
    "'official-sensitive' level\n\nMaximum size: 100MB per file"
)
APPLICATION_GOODS_ADD_DOCUMENT_MISSING = "A document is required"
APPLICATION_GOODS_ADD_PREEXISTING_TITLE = "Add a pre-existing good to your application"

APPLICATION_GOODS_CONTROL_CODE_REQUIRED_DESCRIPTION = (
    "If you don't know, please use "
    + PERMISSION_FINDER_LINK
    + " to find the appropriate code before adding the good to the application. You may need to create a good "
    "from the goods list if you are still unsure."
)

GOODS_CREATE_CONTROL_CODE_REQUIRED_DESC = (
    "If you don't know you can use " + PERMISSION_FINDER_LINK
)
GOODS_CREATE_CONTROL_CODE_NO = "No"
GOODS_CREATE_CONTROL_CODE_YES = "Yes"
GOODS_CREATE_CONTROL_CODE_UNSURE = "I don't know"
GOODS_CREATE_TITLE = "Add a good"

# Applications
APPLICATION_REFERENCE_NAME = "Reference"
APPLICATION_TYPE = "Licence type"
APPLICATION_EXPORT_TYPE = "Export type"
APPLICATION_STATUS = "Status"
APPLICATION_LAST_UPDATED_AT = "Last updated"
APPLICATION_SUBMITTED_AT = "Submitted at"

# Edit application
APPLICATION_EDIT_APPLICATION_BUTTON = "Edit application"

# Withdraw application
APPLICATION_WITHDRAW_ACCESS_BUTTON = "Withdraw application"
APPLICATION_WITHDRAW_TITLE = "Are you sure you want to withdraw this application?"
APPLICATION_WITHDRAW_BACK_TEXT = BACK_TO_APPLICATION
APPLICATION_WITHDRAW_YES_LABEL = YES
APPLICATION_WITHDRAW_NO_LABEL = NO
APPLICATION_WITHDRAW_SUBMIT_BUTTON = SUBMIT
APPLICATION_WITHDRAW_ERROR = 'Select a choice'
