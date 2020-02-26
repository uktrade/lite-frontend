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
    ROLE_NAME = "Role name"
    PERMISSION_CHECKBOXES_TITLE = "Select permissions for the role"
    PERMISSION_CHECKBOXES_DESCRIPTION = ""
    STATUSES_CHECKBOXES_TITLE = "Select statuses the role can set manually"
    STATUSES_CHECKBOXES_DESCRIPTION = ""
    BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Save"


class EditRoleForm:
    TITLE = "Edit role"
    DESCRIPTION = ""
    ROLE_NAME = "Role name"
    PERMISSION_CHECKBOXES_TITLE = "Select permissions for the role"
    PERMISSION_CHECKBOXES_DESCRIPTION = ""
    STATUSES_CHECKBOXES_TITLE = "Select statuses the role can set manually"
    STATUSES_CHECKBOXES_DESCRIPTION = ""
    BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Save"
