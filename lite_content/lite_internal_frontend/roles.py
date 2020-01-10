class ManageRolesPage:
    TAB = "Roles"
    ADD_BUTTON = "Add role"

    class Table:
        HEADER_ROLE = "Role"
        HEADER_PERMISSIONS = "Users with this role "
        EDIT_ROLE = "Edit"


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
    BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Save"
