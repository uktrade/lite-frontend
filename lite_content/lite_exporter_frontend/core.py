class HubPage:
    USERS = "Manage my users"
    SITES = "Manage my sites"
    ROLES = "Manage my roles"
    ORGANISATION = "Manage my organisation"


class ECJUDocumentsTab:
    CREATED_AT = "Created at"
    NONE = "There are no ECJU documents for this product"
    DOWNLOAD_LINK = "Download"


class StartPage:
    TITLE = "Export control account: sign in or set up"
    DESCRIPTION = "You can use your export control account to:"
    BULLET_POINTS = [
        "check if you need an export licence",
        "apply for an export licence",
        "register for an Open General Export Licence",
        "raise an end user advisory query",
        "add products to your database",
    ]
    SIGN_IN_BUTTON = "Sign in with"
    SIGN_IN_BUTTON_SUFFIX = "GREAT"
    OR = "or"
    REGISTER_ACCOUNT_LINK = "register an account"
    NOTICE = (
        "There are different services if you want to export drugs and medicines, export fine art or export livestock"
    )
    BREADCRUMBS = [
        ["Home", "https://gov.uk"],
        ["Business and enterprise", "https://www.gov.uk/topic/business-enterprise"],
        ["Trade restrictions on exports", "https://www.gov.uk/topic/business-enterprise/importing-exporting"],
    ]
