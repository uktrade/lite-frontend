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
    ADD_NAME = "What do you want to call the role?"
    ADD_PERMISSIONS = "What permissions should this role have?"
    ADD_PERMISSIONS_DESCRIPTION = "Select all permissions that apply."
    ADD_FORM_BACK_TO_ROLES = "Back to roles"
    ADD_FORM_CREATE = "Create"


class EditRoleForm:
    TITLE = "Edit a role"
    DESCRIPTION = "This will change this role within your organisation"
    EDIT_NAME = "What do you want to call the role?"
    EDIT_PERMISSIONS = "What permissions should this role have?"
    EDIT_PERMISSIONS_DESCRIPTION = "Select all permissions that apply."
    EDIT_FORM_BACK_TO_ROLES = "Back to roles"
    EDIT_FORM_CREATE = "Create"
