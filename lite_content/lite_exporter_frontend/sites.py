class SitesPage:
    TAB = "Sites"
    ADD_A_SITE_BUTTON = "Add a site"
    EDIT = "Edit "  # Intentional space to separate text and site name
    BACK_TO = "Back to "  # Intentional space to separate text and site name
    PRIMARY_SITE = "(primary site)"

    class Table:
        NAME = "Name"
        ADDRESS = "Address"
        MEMBERS = "Members"
        ACTIONS = "Actions"
        RECORDS_HELD_HERE = "Site where records held"


class SitePage:
    PRIMARY_SITE_DETAIL = "This is your organisation's primary site."
    MEMBERS = "Members"
    ADMIN_MEMBERS = "Admin Members"

    class SummaryList:
        NAME = "Name"
        SITE = "Records held here"
        SITE_ALREADY_USED_ON_APPLICATION_NOTICE = "This site has been used on an application so can’t be edited."


class AddSiteForm:
    BACK_LINK = "Back to " + SitesPage.TAB.lower()

    class WhereIsYourSiteBased:
        TITLE = "Where is your site based?"
        DESCRIPTION = ""
        IN_THE_UK = "In the United Kingdom"
        IN_THE_UK_DESCRIPTION = ""
        OUTSIDE_THE_UK = "Outside of the United Kingdom"
        OUTSIDE_THE_UK_DESCRIPTION = ""
        EXISTING_SITE_ERROR = "Select an option"
        ERROR = "Select a location"

    class Details:
        TITLE = "Site details"
        DESCRIPTION = ""
        NAME = "Name"
        ADDRESS_HEADER_UK = "Where in the United Kingdom is your site based?"
        ADDRESS_HEADER_ABROAD = "Where is your site based?"

    class Postcode:
        TITLE = "There's already a site registered with this postcode"
        DESCRIPTION = "This postcode is already registered for {}. You should not add this site unless it is a different site at the same postcode."
        CONTROL_TITLE = "Are you sure you want to continue?"
        YES = "Yes, continue"
        NO = "No"

    class AssignUsers:
        TITLE = "Assign users to the site (optional)"
        DESCRIPTION = (
            "Users with the permission to manage sites will still be able to access the site. "
            "You can still assign users later."
        )
        FILTER = "Filter users"

    class SiteRecords:
        DESCRIPTION = "ECJU uses this for compliance visits."

        class SiteInUK:
            TITLE = "Are the records for licences registered to this site held here?"
            NO_RECORDS_HELD_ELSEWHERE = "No, company records are held at another site"
            SITE_NOT_LISTED = "If the site isn't listed, you need to add the site from your account dashboard."

        class SiteNotInUK:
            TITLE = "Select the site that holds the licence records for the non-UK based site you’re adding"
