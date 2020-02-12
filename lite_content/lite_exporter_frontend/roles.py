class ManageRolesPage:
    TAB = "Roles"
    ADD_BUTTON = "Add a role"

    class Table:
        HEADER_ROLE = "Role"
        HEADER_PERMISSIONS = "Members with this role "
        EDIT_ROLE = "Edit"


class AddRoleForm:
    TITLE = "Add a role"
    DESCRIPTION = ""
    NAME = "Role name"
    PERMISSIONS = "Permissions"
    PERMISSIONS_DESCRIPTION = ""
    FORM_BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Save"


class EditRoleForm:
    TITLE = "Edit role"
    DESCRIPTION = ""
    NAME = "Role name"
    PERMISSIONS = "Permissions"
    PERMISSIONS_DESCRIPTION = ""
    FORM_BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Save"
