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
