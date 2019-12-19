class ManageRolesPage:
    TAB = "Roles"
    ADD_BUTTON = "Add role"

    class Table:
        HEADER_ROLE = "Role"
        HEADER_PERMISSIONS = "Users with this role "
        EDIT_ROLE = "Edit"


class AddRoleForm:
    TITLE = "Add a role"
    DESCRIPTION = "This will create a new role to use within your organisation"
    NAME = "What do you want to call the role?"
    PERMISSIONS = "What permissions should this role have?"
    PERMISSIONS_DESCRIPTION = "Select all permissions that apply."
    FORM_BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Create"


class EditRoleForm:
    TITLE = "Edit a role"
    DESCRIPTION = "This will change this role within your organisation"
    NAME = "What do you want to call the role?"
    PERMISSIONS = "What permissions should this role have?"
    PERMISSIONS_DESCRIPTION = "Select all permissions that apply."
    FORM_BACK_TO_ROLES = "Back to roles"
    FORM_CREATE = "Create"
