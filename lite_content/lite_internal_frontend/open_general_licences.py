OGEL_DESCRIPTION = (
    "Licence which allows the export of specified controlled items by any exporter, removing "
    "the need for them to apply for an individual licence."
)
OGTCL_DESCRIPTION = (
    "Licences which control the trafficking and brokering activity between one third country "
    "and another where the transaction or deal is brokered in the UK or by a UK person."
)
OGTL_DESCRIPTION = (
    "Transhipment licences allow controlled goods to pass through the UK on the way to other " "destinations."
)


class List:
    TITLE = "Open general licences"
    ADD_AN_OGL_BUTTON = "Add an open general licence"
    NO_CONTENT = "No open general licences added"

    class Filters:
        NAME = "name"
        TYPE = "type"
        CONTROL_LIST_ENTRY = "control list entry"
        COUNTRY = "country"

    class Tabs:
        ACTIVE = "Active"
        DEACTIVATED = "Deactivated"

    class Table:
        NAME = "Name"
        TYPE = "Type"
        DESCRIPTION = "Description"
        REGISTRATION_REQUIRED = "Registration required"
        MORE_INFORMATION = "More information"
        APPLIES_TO = "Applies to"
        CONTROL_LIST_ENTRIES = "control list entry/control list entries"
        COUNTRIES = "country/countries"
        READ_ON_GOVUK_LINK = "Read on GOV.UK"


class Detail:
    BACK_LINK = "Back to " + List.TITLE.lower()
    ACTIVITY = "Activity"

    class SummaryList:
        NAME = "Name"
        TYPE = "Type"
        DESCRIPTION = "Description"
        REGISTRATION_REQUIRED = "Registration required"
        LINK = "Link"
        STATUS = "Status"
        CREATED_AT = "Created at"
        UPDATED_AT = "Updated at"
        CONTROL_LIST_ENTRIES = "Control list entry/Control list entries"
        COUNTRIES = "Country/Countries"
        DEACTIVATE_LINK = "Deactivate <!--OGL-->"
        REACTIVATE_LINK = "Reactivate <!--OGL-->"

    class ActivityFilters:
        USER = "user"
        TEAM = "team"
        USER_TYPE = "user type"
        ACTIVITY_TYPE = "activity type"
        DATE_FROM = "date from"
        DATE_TO = "date to"
        NO_ACTIVITIES = "No activities match your filters"


class Create:
    SUMMARY_TITLE = "Confirm details about this "
    SUBMIT_BUTTON = "Submit"
    SUCCESS_MESSAGE = "Open general licence added successfully"

    class Steps:
        STEP_1 = "Step 1 of 4"
        STEP_2 = "Step 2 of 4"
        STEP_3 = "Step 3 of 4"
        STEP_4 = "Step 4 of 4"

    class SelectType:
        TITLE = "Select the type of open general licence you want to add"
        DESCRIPTION = ""

    class Details:
        TITLE = "Provide details about the {}"
        DESCRIPTION = ""

        class Name:
            TITLE = "What's the name of the {} you want to add?"
            SHORT_TITLE = "Name"
            DESCRIPTION = (
                "Use the name from GOV.UK. For example, 'Military goods, software and technology: "
                "government or NATO end use'"
            )

        class Description:
            TITLE = "Description"
            SHORT_TITLE = "Description"
            DESCRIPTION = "Use the description provided by GOV.UK (if possible)"

        class Link:
            TITLE = "Link to the {}"
            SHORT_TITLE = "Link"
            DESCRIPTION = (
                "Only link to GOV.UK pages. For example, 'https://www.gov.uk/government/publications/"
                "open-general-export-licence-military-goods-government-or-nato-end-use--6'"
            )

        class RequiresRegistration:
            TITLE = "Does this {} require registration?"
            SHORT_TITLE = "Requires registration"
            DESCRIPTION = "Select 'Yes' if an exporter has to register the {} to use it"
            YES = "Yes"
            NO = "No"

    class ControlListEntries:
        TITLE = "Select applicable control list entries"
        SHORT_TITLE = "Control list entries"
        DESCRIPTION = ""

    class Countries:
        TITLE = "Select applicable countries"
        SHORT_TITLE = "Countries"
        DESCRIPTION = ""


class Edit:
    SUCCESS_MESSAGE = "Open general licence saved successfully"
    SELECT_OPTION = "Select an option"

    class Steps:
        STEP_1 = "Step 1 of 4"
        STEP_2 = "Step 2 of 4"
        STEP_3 = "Step 3 of 4"
        STEP_4 = "Step 4 of 4"

    class SelectType:
        TITLE = "Select the type of open general licence you want to add"
        DESCRIPTION = ""

    class Details:
        TITLE = "Edit details"
        DESCRIPTION = ""

        class Name:
            TITLE = "What's the name of this {}?"
            SHORT_TITLE = "Name"
            DESCRIPTION = (
                "Use the name from GOV.UK. For example, 'Military goods, software and technology: "
                "government or NATO end use'"
            )

        class Description:
            TITLE = "Description"
            SHORT_TITLE = "Description"
            DESCRIPTION = "Use the description provided by GOV.UK (if possible)"

        class Link:
            TITLE = "Link to the {}"
            SHORT_TITLE = "Link"
            DESCRIPTION = (
                "Only link to GOV.UK pages. For example, 'https://www.gov.uk/government/publications/"
                "open-general-export-licence-military-goods-government-or-nato-end-use--6'"
            )

        class RequiresRegistration:
            TITLE = "Does this {} require registration?"
            SHORT_TITLE = "Requires registration"
            DESCRIPTION = "Select 'Yes' if an exporter has to register the {} to use it"
            YES = "Yes"
            NO = "No"

    class ControlListEntries:
        TITLE = "Change applicable control list entries"
        SHORT_TITLE = "Control list entries"
        DESCRIPTION = ""

    class Countries:
        TITLE = "Change applicable countries"
        SHORT_TITLE = "Countries"
        DESCRIPTION = ""


class Reactivate:
    TITLE = "Are you sure you want to reactivate {}?"
    DESCRIPTION = "This will allow exporters to use this licence. You can change this in the future"
    BACK_LINK = "Back to {}"
    YES = "Yes"
    NO = "No"
    SUBMIT_BUTTON = "Submit"
    SUCCESS_MESSAGE = "Open general licence reactivated successfully"


class Deactivate:
    TITLE = "Are you sure you want to deactivate {}?"
    DESCRIPTION = "This will prevent exporters from using this licence. You can change this in the future"
    BACK_LINK = "Back to {}"
    YES = "Yes"
    NO = "No"
    SUBMIT_BUTTON = "Submit"
    SUCCESS_MESSAGE = "Open general licence deactivated successfully"
