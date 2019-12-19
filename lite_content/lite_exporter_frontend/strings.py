from conf.settings import env
from lite_content.lite_exporter_frontend import applications, goods

APPLICATIONS = applications
GOODS = goods

# Generic
BACK_TO_APPLICATION = "Back to application"
YES = "Yes"
NO = "No"
SUBMIT = "Submit"
SAVE = "Save"
CONTINUE = "Continue"
SAVE_AND_CONTINUE = "Save and continue"
CANCEL = "Cancel"
POST_NOTE = "Post note"

THIS_SECTION_IS = "This section is "  # The space at the end is intentional. Usage is 'This section is optional'
OPTIONAL = "Optional"
NOT_STARTED = "Not started"
IN_PROGRESS = "In progress"
DONE = "Completed"
VIEW = "View"

PERMISSION_FINDER_LINK = "[control list](" + env("PERMISSIONS_FINDER_URL") + ")"

APPLICATION_GOODS_CONTROL_CODE_REQUIRED_DESCRIPTION = (
    "Products that aren't on the "
    + PERMISSION_FINDER_LINK
    + " may be affected by military end use controls, current trade sanctions and embargoes or weapons of mass destruction controls."
    "If your products aren't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
)

GOODS_CREATE_CONTROL_CODE_REQUIRED_DESC = "If you don't know, you can use the " + PERMISSION_FINDER_LINK
GOODS_CREATE_CONTROL_CODE_NO = "No"
GOODS_CREATE_CONTROL_CODE_YES = "Yes"
GOODS_CREATE_CONTROL_CODE_UNSURE = "I don't know"
GOODS_CREATE_TITLE = "Add a product"

# Applications
APPLICATION_REFERENCE_NAME = "Reference"
APPLICATION_TYPE = "Licence type"
APPLICATION_EXPORT_TYPE = "Export type"
APPLICATION_STATUS = "Status"
APPLICATION_LAST_UPDATED_AT = "Last updated"
APPLICATION_CREATED_AT = "Created at"
APPLICATION_SUBMITTED_AT = "Submitted at"

APPLICATION_END_USER = "End user"
APPLICATION_ULTIMATE_END_USERS = "Ultimate recipient"
APPLICATION_CONSIGNEE = "Consignee"
APPLICATION_THIRD_PARTIES = "Third parties"
APPLICATION_GOODS_LOCATIONS = "Product locations"
APPLICATION_SUPPORTING_DOCUMENTATION = "Supporting documentation"
APPLICATION_GOODS = "Products"
APPLICATION_COUNTRIES = "Countries"
APPLICATION_ON_BEHALF_OF = "On behalf of"
APPLICATION_OPTIONAL_NOTE = "Optional note"

# Initial application questions
WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE = "Select the type of licence you need"
WHICH_EXPORT_LICENCE_DO_YOU_WANT_DESCRIPTION = ""

STANDARD_LICENCE = "Standard licence"
STANDARD_LICENCE_DESCRIPTION = "Select a standard licence for a set quantity and set value of products."
OPEN_LICENCE = "Open licence"
OPEN_LICENCE_DESCRIPTION = (
    "Select an open licence for multiple shipments of specific products to specific countries. "
    "Open licences cover long term projects and repeat business."
)

HELP_WITH_CHOOSING_A_LICENCE = "Help with choosing a licence"
HELP_WITH_CHOOSING_A_LICENCE_CONTENT = (
    "If you're unsure about which licence to select, read the guidance on "
    'GOV.UK for <a class="govuk-link" target="_blank" '
    'href="https://www.gov.uk/starting-to-export/licences">exporting and doing business '
    'abroad<span class="govuk-visually-hidden"> (opens in a new window or tab)</span></a>.'
)

ENTER_A_REFERENCE_NAME_TITLE = "Application reference"
ENTER_A_REFERENCE_NAME_SHORT_TITLE = "Reference name"
ENTER_A_REFERENCE_NAME_DESCRIPTION = "Name and save this application so you can refer back to it when needed."

TEMPORARY_OR_PERMANENT_TITLE = "Select an export type"
TEMPORARY_OR_PERMANENT_DESCRIPTION = ""

TEMPORARY = "Temporary"
PERMANENT = "Permanent"

HAVE_YOU_BEEN_INFORMED_TITLE = "Have you been informed under an end use control that you need to apply for a licence?"
HAVE_YOU_BEEN_INFORMED_DESCRIPTION = "This could be a letter or email from HMRC or another government department."
WHAT_WAS_THE_REFERENCE_CODE_TITLE = "Reference number (optional)"
WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION = "The reference number is on the letter or email."

WHERE_ARE_YOUR_GOODS_GOING_TITLE = "Where are your products going?"
WHERE_ARE_YOUR_GOODS_GOING_SHORT_TITLE = "Set countries"
WHERE_ARE_YOUR_GOODS_GOING_DESCRIPTION = "Select all countries that apply."

# Edit application
APPLICATION_EDIT_APPLICATION_BUTTON = "Edit application"

# Delete draft
DRAFT_DELETE_LINK = "Delete draft"
DRAFT_DELETE_TITLE = "Are you sure you want to delete this draft?"
DRAFT_DELETE_BACK_TEXT = BACK_TO_APPLICATION
DRAFT_DELETE_YES_LABEL = YES
DRAFT_DELETE_NO_LABEL = NO
DRAFT_DELETE_SUBMIT_BUTTON = SUBMIT
DRAFT_DELETE_ERROR = "Select a choice"

# Withdraw application
APPLICATION_WITHDRAW_ACCESS_BUTTON = "Withdraw application"
APPLICATION_WITHDRAW_TITLE = "Are you sure you want to withdraw this application?"
APPLICATION_WITHDRAW_BACK_TEXT = BACK_TO_APPLICATION
APPLICATION_WITHDRAW_YES_LABEL = YES
APPLICATION_WITHDRAW_NO_LABEL = NO
APPLICATION_WITHDRAW_SUBMIT_BUTTON = SUBMIT
APPLICATION_WITHDRAW_ERROR = "Select a choice"

# Roles
ROLES_LIST_PAGE_CREATE = "Add role"
APPLICATION_WHERE_ARE_YOUR_GOODS_LOCATED_TITLE = "Where are your products located?"
APPLICATION_WHERE_ARE_YOUR_GOODS_LOCATED_DESCRIPTION = ""
APPLICATION_ONE_OF_MY_REGISTERED_SITES = "At one of my organisation’s sites"
APPLICATION_NOT_AT_MY_REGISTERED_SITES = "At a location that's not part of my organisation"

APPLICATION_EXTERNAL_LOCATION_TITLE = "Do you want to add a new external location or use an existing one?"
APPLICATION_EXTERNAL_LOCATION_NEW_LOCATION = "Add a new external location"
APPLICATION_EXTERNAL_LOCATION_PREEXISTING_LOCATION = "Use an existing external location"

SELECT_SITES_TITLE = "Select which sites your products are at"
SELECT_SITES_BUTTON = "Select sites"

USERS_LIST_PAGE_EDIT = "Edit"

USER_PROFILE_PAGE_EDIT = "Edit"
USER_PROFILE_BACK_TO_USERS = "Back to users"

USER_ROLE_QUESTION = "What role should this user have?"

USER_ADD_TITLE = "Add new user"
USER_EMAIL_QUESTION = "Whats the user's email"
USER_ADD_FORM_BACK_TO_USERS = "Back to users"
USER_EDIT_TITLE = "Change role"
USER_EDIT_FORM_BACK_TO_USER = "Back to user"
USER_EDIT_FORM_SAVE = "Save"

USER_EMAIL = "Email"
USER_NAME = "Name"
USER_FIRST_NAME = "First name"
USER_LAST_NAME = "Last name"
USER_ROLE = "Role"
USER_STATUS = "Status"
USER_PENDING = "Pending"

USER_DEACTIVATE = "Deactivate user"
USER_REACTIVATE = "Reactivate user"
USER_NOT_ACTIVATED_YET = "This user has yet to sign in to their export control account."

MANAGE_ORGANISATIONS_MEMBERS_TAB = "Members"
MANAGE_ORGANISATIONS_SITES_TAB = "Sites"
MANAGE_ORGANISATIONS_ROLES_TAB = "Roles"

ROLE_INDEX_TABLE_HEADER_ROLE = "Role"
ROLE_INDEX_TABLE_HEADER_PERMISSIONS = "Users with this role "
ROLE_INDEX_TABLE_EDIT_ROLE = "Edit"

ADD_ROLE_TITLE = "Add a role"
ADD_ROLE_DESCRIPTION = "This will create a new role to use within your organisation"
EDIT_ROLE_TITLE = "Edit a role"
EDIT_ROLE_DESCRIPTION = "This will change this role within your organisation"
ROLES_ADD_NAME = "What do you want to call the role?"
ROLES_ADD_PERMISSIONS = "What permissions should this role have?"
ROLES_ADD_PERMISSIONS_DESCRIPTION = "Select all permissions that apply."
ROLES_ADD_FORM_BACK_TO_ROLES = "Back to roles"
ROLES_ADD_FORM_CREATE = "Create"
ROLES_EDIT_NAME = "What do you want to call the role?"
ROLES_EDIT_PERMISSIONS = "What permissions should this role have?"
ROLES_EDIT_PERMISSIONS_DESCRIPTION = "Select all permissions that apply."
ROLES_EDIT_FORM_BACK_TO_ROLES = "Back to roles"
ROLES_EDIT_FORM_CREATE = "Create"


HUB_MANAGE_MY_USERS = "Manage my users"
HUB_MANAGE_MY_SITES = "Manage my sites"
HUB_MANAGE_MY_ROLES = "Manage my roles"
HUB_MANAGE_MY_ORGANISATION = "Manage my organisation"


SUBMIT_APPLICATION = "Submit application"
EDIT_APPLICATION_SUBMIT = "Submit application"
EDIT_APPLICATION_DONE = "Done"

COPY_END_USER_ADVISORY_BACK_TO_END_USER_ADVISORIES = "Back to end user advisories"

NOTIFICATIONS = "Notifications"

UPLOAD_FAILURE_ERROR = "We had an issue uploading your files. Try again later."
UPLOAD_GENERIC_ERROR = "We had an issue creating your response. Try again later."
DOWNLOAD_GENERIC_ERROR = "We had an issue downloading your file. Try again later."

DOCUMENT_DELETE_GENERIC_ERROR = "We had an issue deleting your files. Try again later."
