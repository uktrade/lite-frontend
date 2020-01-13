class ManageRolesPage:
    ADD_BUTTON = "Create a new role"
    DESCRIPTION = "Roles define permissions for users to perform a set of tasks"
    TAB = "Roles"
    TITLE = "Roles"

    class Table:
        EDIT_BUTTON = "Edit"
        HEADER = "Role"
        PERMISSIONS_TITLE = "Users with this role can"


class AddRoleForm:
    TITLE = "Create a new role"
    DESCRIPTION = ""
    ROLE_NAME = "What do you want to call the role?"
    PERMISSION_CHECKBOXES_TITLE = "Select the permissions this role has"
    PERMISSION_CHECKBOXES_DESCRIPTION = ""
    STATUSES_CHECKBOXES_TITLE = "Select the statuses this role can set manually"
    STATUSES_CHECKBOXES_DESCRIPTION = ""
    BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Save"


class EditRoleForm:
    TITLE = "Edit role"
    DESCRIPTION = ""
    ROLE_NAME = "What do you want to call the role?"
    PERMISSION_CHECKBOXES_TITLE = "Select the permissions this role has"
    PERMISSION_CHECKBOXES_DESCRIPTION = ""
    STATUSES_CHECKBOXES_TITLE = "Select the statuses this role can set manually"
    STATUSES_CHECKBOXES_DESCRIPTION = ""
    FORM_BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Save"
