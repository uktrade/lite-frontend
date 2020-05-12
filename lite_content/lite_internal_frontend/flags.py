class FlagsList:
    TITLE = "Flags"
    DESCRIPTION = "Flags are a simple way to tag cases, organisations, destinations and goods."
    CREATE_BUTTON = "Create a flag"
    NO_CONTENT_NOTICE = "There are no registered flags at the moment."
    SUCCESS_MESSAGE = "Flag created successfully"
    SHOW_DEACTIVATED_FLAGS = "Only show deactivated flags"

    class Table:
        NAME = "Name"
        TEAM = "Team"
        LEVEL = "Level"
        LABEL = "Label"
        PRIORITY = "Priority"
        BLOCKS_APPROVAL = "Blocks Approval"
        STATUS = "Status"
        ACTIONS = "Actions"
        REACTIVATE = "Reactivate"
        DEACTIVATE = "Deactivate"
        EDIT = "Edit"


class CreateFlagForm:
    BACK_LINK = "Back to " + FlagsList.TITLE.lower()
    TITLE = "Create a flag"
    DESCRIPTION = ""
    SUBMIT_BUTTON = "Create"

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""

    class Level:
        TITLE = "Level"
        DESCRIPTION = ""

    class Colour:
        TITLE = "Colour"
        DESCRIPTION = "You can help convey information through use of colour"

    class Label:
        TITLE = "Colour meaning"
        DESCRIPTION = "We'll show this value when you hover over the flag to provide more information"

    class Priority:
        TITLE = "Priority"
        DESCRIPTION = "This relates to the ordering of the flag. 0 is the highest."

    class BlocksApproval:
        TITLE = "Blocks application approval"
        YES = "Yes"
        NO = "No"


class EditFlagForm:
    BACK_LINK = "Back to " + FlagsList.TITLE.lower()
    TITLE = "Edit flag"
    DESCRIPTION = ""
    SUBMIT_BUTTON = "Save and return"

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""

    class Colour:
        TITLE = "Colour"
        DESCRIPTION = "You can help convey information through use of colour"

    class Label:
        TITLE = "Colour meaning"
        DESCRIPTION = "We'll show this value when you hover over the flag to provide more information"

    class Priority:
        TITLE = "Priority"
        DESCRIPTION = "This relates to the ordering of the flag. 0 is the highest."

    class BlocksApproval:
        TITLE = "Blocks application approval"
        YES = "Yes"
        NO = "No"


class UpdateFlag:
    class Status:
        DEACTIVATE_HEADING = "Are you sure you want to deactivate this flag?"
        DEACTIVATE_WARNING = "This flag will no longer be able to be used unless it's reactivated"
        REACTIVATE_HEADING = "Are you sure you want to reactivate this flag?"
        REACTIVATE_WARNING = "This flag will be able to be used unless it's deactivated again"


class SetFlagsForm:
    class Cases:
        TITLE = "Set case flags"
        DESCRIPTION = "Select all flags that you want to set on this case."
        SUBMIT_BUTTON = "Set flags"
        SUCCESS_MESSAGE = "Flags set successfully on case"
        FILTER = "Filter"

        class Note:
            TITLE = "Specify why you're changing this case's flags (optional)"

    class Organisations:
        TITLE = "Set organisation flags"
        DESCRIPTION = "Select all flags that you want to set on this organisation."
        SUBMIT_BUTTON = "Set flags"
        SUCCESS_MESSAGE = "Flags set successfully on organisation"
        FILTER = "Filter"

        class Note:
            TITLE = "Specify why you're changing this organisation's flags (optional)"

    class Goods:
        TITLE = "Set goods flags"
        DESCRIPTION = "Select all flags that you want to set on these goods."
        SUBMIT_BUTTON = "Set flags"
        SUCCESS_MESSAGE = "Flags set successfully on good(s)"
        FILTER = "Filter"

        class Note:
            TITLE = "Specify why you're changing the flags (optional)"

    class Destinations:
        TITLE = "Set destination flags"
        DESCRIPTION = "Select all flags that you want to set on these destinations."
        SUBMIT_BUTTON = "Set flags"
        SUCCESS_MESSAGE = "Flags set successfully on destination(s)"
        FILTER = "Filter"

        class Note:
            TITLE = "Specify why you're changing the flags (optional)"
