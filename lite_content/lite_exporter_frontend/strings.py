from conf.settings import env

# Generic
BACK_TO_APPLICATION = "Back to application"
YES = "Yes"
NO = "No"
SUBMIT = "Submit"
SAVE = "Save"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"

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

# Initial application questions
WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE = (
    "Which export licence do you want to apply for?"
)
WHICH_EXPORT_LICENCE_DO_YOU_WANT_DESCRIPTION = "Select one of the options."

STANDARD_LICENCE = "Standard Licence"
STANDARD_LICENCE_DESCRIPTION = "Standard Licences are specific to the company and the recipient (consignee). " \
                               "They are for a set quantity and set value of goods. You will need to provide support " \
                               "documentation with your application."
OPEN_LICENCE = "Open Licence"
OPEN_LICENCE_DESCRIPTION = "Open Licences cover long-term projects and repeat business. This is company specific, " \
                           "with no set quantity or value of goods. You will receive compliance audits under this type of licence."

HELP_WITH_CHOOSING_A_LICENCE = "Help with choosing a licence"
HELP_WITH_CHOOSING_A_LICENCE_CONTENT = 'If you\'re unsure about which licence to select, then read the guidance on ' \
                                       'GOV.UK for <a class="govuk-link" target="_blank" ' \
                                       'href="https://www.gov.uk/starting-to-export/licences">exporting and doing business ' \
                                       'abroad<span class="govuk-visually-hidden"> (Opens in a new window or tab)</span></a>.'

ENTER_A_REFERENCE_NAME_TITLE = "Enter a reference name for your application"
ENTER_A_REFERENCE_NAME_DESCRIPTION = (
    "This can make it easier for you or your organisation to find in the future."
)

TEMPORARY_OR_PERMANENT_TITLE = "Do you want to export temporarily or permanently?"
TEMPORARY_OR_PERMANENT_DESCRIPTION = ""

TEMPORARY = "Temporarily"
PERMANENT = "Permanently"

HAVE_YOU_BEEN_INFORMED_TITLE = (
    "Have you been told that you need an export licence by an official?"
)
HAVE_YOU_BEEN_INFORMED_DESCRIPTION = (
    "This could be a letter or email from HMRC or another government department."
)
WHAT_WAS_THE_REFERENCE_CODE_TITLE = (
    "What was the reference number if you were provided one?"
)
WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION = "This is the reference found on the letter or email to tell you to apply for an export licence."

# Edit application
APPLICATION_EDIT_APPLICATION_BUTTON = "Edit application"

# Withdraw application
APPLICATION_WITHDRAW_ACCESS_BUTTON = "Withdraw application"
APPLICATION_WITHDRAW_TITLE = "Are you sure you want to withdraw this application?"
APPLICATION_WITHDRAW_BACK_TEXT = BACK_TO_APPLICATION
APPLICATION_WITHDRAW_YES_LABEL = YES
APPLICATION_WITHDRAW_NO_LABEL = NO
APPLICATION_WITHDRAW_SUBMIT_BUTTON = SUBMIT
APPLICATION_WITHDRAW_ERROR = "Select a choice"
