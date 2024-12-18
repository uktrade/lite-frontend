class HubPage:
    ORGANISATION = "Manage my organisation"


class ECJUDocumentsTab:
    CREATED_AT = "Created at"
    NONE = "There are no ECJU documents for this product."
    DOWNLOAD_LINK = "Download"


class StartPage:
    # Once we have GOV.UK sign-in integrated this can be removed or merged with  StartPageGovUK
    TITLE = "Export control account: sign in or set up"
    DESCRIPTION = "You can use your export control account to:"
    BULLET_POINTS = [
        "check if you need an export licence",
        "apply for an export licence",
        "register for an Open General Export Licence",
        "raise an end user advisory query",
        "add products to your database",
    ]
    SIGN_IN_BUTTON = "Sign in with GOV.UK"
    SIGN_IN_BUTTON_SUFFIX = "GOV.UK"
    OR = "or"
    REGISTER_ACCOUNT_LINK = "set up an account"

    BREADCRUMBS = [
        ["Home", "https://gov.uk"],
        ["Business and enterprise", "https://www.gov.uk/topic/business-enterprise"],
        ["Trade restrictions on exports", "https://www.gov.uk/topic/business-enterprise/importing-exporting"],
    ]


class StartPageGovUK:
    TITLE = "Apply for a standard individual export licence (SIEL)"
    BULLET_POINTS = [
        "apply for a SIEL to export goods or products",
        "edit or check an application",
        "view your existing SIELs",
    ]
    DESCRIPTION = "Use this service to:"
    SIGN_IN_BUTTON = "Start now >"
    SIGN_IN_BUTTON_SUFFIX = "GOV.UK"
    OR = "or"
    REGISTER_ACCOUNT_LINK = "set up an account"

    BREADCRUMBS = [
        ["Home", "https://gov.uk"],
        ["Business and enterprise", "https://www.gov.uk/topic/business-enterprise"],
        ["Trade restrictions on exports", "https://www.gov.uk/topic/business-enterprise/importing-exporting"],
    ]


class RegisterAnOrganisation:
    class Landing:
        TITLE = "Create an export control account"
        DESCRIPTION = (
            "To use this service, you need to register with the Export Control Joint Unit "
            "(ECJU) for an export control account."
        )
        DESCRIPTION_2 = (
            "If you work for an organisation, check with your colleagues first before creating "
            "an account as your organisation might already be registered. If your organisation "
            "does have an export control account, ask a super user to add you as a team member."
        )
        SUMMARY_LIST_HEADER = "Once approved, you can use your account to: "
        BUTTON = "Create an account"

    class CommercialOrIndividual:
        TITLE = "Commercial organisation or private individual"
        DESCRIPTION = ""
        COMMERCIAL = "Commercial organisation"
        COMMERCIAL_DESCRIPTION = "Select this if you want to register an organisation that will be exporting"
        INDIVIDUAL = "Private individual"
        INDIVIDUAL_DESCRIPTION = "Select this if you're a private individual that will be exporting alone"
        ERROR = "Select the type of organisation you're registering for"

    class WhereIsYourOrganisationBased:
        TITLE = "Where is your organisation based?"
        DESCRIPTION = ""
        IN_THE_UK = "In the United Kingdom"
        IN_THE_UK_DESCRIPTION = ""
        OUTSIDE_THE_UK = "Outside of the United Kingdom"
        OUTSIDE_THE_UK_DESCRIPTION = ""
        ERROR = "Select a location"

    class Commercial:
        TITLE = "Register a commercial organisation"
        DESCRIPTION = ""
        NAME = "Name of organisation"
        NAME_DESCRIPTION = ""
        EORI_NUMBER = "European Union registration and identification number (EORI)"
        EORI_NUMBER_DESCRIPTION = "[Get an EORI number](https://www.gov.uk/eori) if you don't have one."
        EORI_NUMBER_SHORT_TITLE = "EORI number"
        SIC_NUMBER = "SIC code"
        SIC_NUMBER_DESCRIPTION = (
            "[Find your SIC code](https://www.gov.uk/government/publications/standard-industria"
            "l-classification-of-economic-activities-sic)."
        )
        SIC_NUMBER_SHORT_TITLE = "SIC code"
        VAT_NUMBER = "UK VAT number"
        VAT_NUMBER_DESCRIPTION = (
            "9 digits long, with the first 2 letters indicating the country code of the registered business."
        )
        VAT_NUMBER_SHORT_TITLE = "UK VAT number"
        CRN_NUMBER = "Companies House registration number (CRN)"
        CRN_NUMBER_DESCRIPTION = "8 numbers, or 2 letters followed by 6 numbers."
        CRN_NUMBER_SHORT_TITLE = "CRN number"

    class Individual:
        TITLE = "Register a private individual"
        DESCRIPTION = ""
        NAME = "First and last name"
        NAME_DESCRIPTION = ""
        EORI_NUMBER = "European Union registration and identification number (EORI)"
        EORI_NUMBER_DESCRIPTION = "[Get an EORI number](https://www.gov.uk/eori) if you don't have one."
        EORI_NUMBER_SHORT_TITLE = "EORI number"
        VAT_NUMBER = "UK VAT number"
        VAT_NUMBER_DESCRIPTION = (
            "9 digits long, with the first 2 letters indicating the country code of the registered business."
        )
        VAT_NUMBER_SHORT_TITLE = "UK VAT number"

    class Headquarters:
        TITLE = "What is your registered office address?"
        TITLE_FOREIGN = "Where is your organisation based?"
        TITLE_INDIVIDUAL = "Where in the United Kingdom are you based?"
        TITLE_INDIVIDUAL_FOREIGN = "Where are you based?"
        DESCRIPTION = ""
        NAME = "Name of headquarters"
        NAME_DESCRIPTION = ""
        FORM_HELP_TITLE = "Help with your registered office address"
        FORM_HELP_DESCRIPTION = (
            "This is usually the office address registered with Companies House. "
            "Or HM Revenue and Customs if you're not on Companies House.\n "
            "Your organisation might have multiple sites or business addresses, "
            "but there will only be one registered office."
        )


class Errors:
    PERMISSION_DENIED = "You do not have permission to access this resource"
