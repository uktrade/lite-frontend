TITLE = "Exporter hub"
ACCOUNT = "Export control account"


class Header:
    ACCOUNT_HOME = "Account home"
    SWITCH_ORG = "Switch organisation"


class Navigation:
    ACCOUNT_HOME = "Account home"
    YOUR_ACCOUNT = "Manage your organisation and personal details"


class Tiles:
    APPLY_FOR_LICENCE = "Apply"
    APPLICATIONS = "Applications"
    VIEW_AND_MANAGE_LICENCES = "View and manage licences and clearances"
    GOODS = "Product list"
    END_USER_ADVISORIES = "End user advisories"

    # Standard dashboard
    class Apply:
        APPLY_FOR = "Apply for:"
        EXPORT_LICENCES = "export licences"
        TRANSHIPMENT_LICENCES = "transhipment licences"
        TRADE_CONTROL_LICENCES = "trade control licences"
        MOD_CLEARANCES = "MOD clearances"
        REGISTER_OGEL = "Register for open general export licences (OGELs)."

    class Applications:
        CHECK_PROGRESS = "Check the progress of submitted applications and registrations."
        EDIT_APPLICATIONS = "Edit, withdraw or copy applications."

    class Licences:
        # Blank for now for Anthony to add to tile later
        DESCRIPTION = ""

    class ProductList:
        MANAGE_PRODUCTS = "View and manage your organisation's product database."
        PRODUCTS_INCLUDE = "Products include goods, items, technology, data and services."
        CLC_LINK = "Create a control list classification (CLC) query"
        GRADING_LINK = "Apply for a security grading"

    class EUA:
        ASK_FOR_ADVICE = "Ask for advice about any overseas company, government or individual in your export."

    # HMRC Dashboard
    class CustomsEnquiry:
        MAKE_ENQUIRY = "Make a customs enquiry"
        DRAFT_LINK = "Draft applications"

    class CheckProgress:
        TITLE = "Check progress"
        VIEW_STATUS = "View the status of your enquiries."
