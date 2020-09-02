from lite_content.lite_internal_frontend.users import UsersPage


class ManageRolesPage:
    BACK_LINK = "Back to " + UsersPage.TITLE.lower()
    TITLE = "Roles"
    DESCRIPTION = "Roles define permissions for users to perform a set of tasks"
    ADD_BUTTON = "Create a new role"
    SUCCESS_MESSAGE = "Role created successfully"

    class Table:
        HEADER = "Role"
        PERMISSIONS_TITLE = "Users with this role can"
        ACTIONS = "Actions"
        EDIT = "Edit"


class AddRoleForm:
    BACK_LINK = "Back to " + ManageRolesPage.TITLE.lower()
    TITLE = "Create a new role"
    DESCRIPTION = ""
    ROLE_NAME = "Role name"
    PERMISSION_CHECKBOXES_TITLE = "Select permissions for the role"
    PERMISSION_CHECKBOXES_DESCRIPTION = ""
    STATUSES_CHECKBOXES_TITLE = "Select statuses the role can set manually"
    STATUSES_CHECKBOXES_DESCRIPTION = ""
    FORM_CREATE = "Save"


class EditRoleForm:
    BACK_LINK = "Back to " + ManageRolesPage.TITLE.lower()
    TITLE = "Edit role"
    DESCRIPTION = ""
    ROLE_NAME = "Role name"
    PERMISSION_CHECKBOXES_TITLE = "Select permissions for the role"
    PERMISSION_CHECKBOXES_DESCRIPTION = ""
    STATUSES_CHECKBOXES_TITLE = "Select statuses the role can set manually"
    STATUSES_CHECKBOXES_DESCRIPTION = ""
    FORM_CREATE = "Save"
