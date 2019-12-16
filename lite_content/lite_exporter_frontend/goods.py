from lite_content.lite_exporter_frontend.strings import PERMISSION_FINDER_LINK


class DocumentSensitivityForm:
    TITLE = "Does your good meet the following criteria?"
    DESCRIPTION = (
        "I have a document for my good\nThe document is below official-sensitive in rating\nThe document "
        "is not commercially sensitive"
    )
    ECJU_HELPLINE = (
        "You need to contact the Export Control Joint Unit (ECJU). They will arrange a secure way for you "
        "to share this document.\n\nPhone: 020 7215 4594\n\nYou can continue using the system in the "
        "meantime "
    )

    class Options:
        YES = "Yes"
        NO = "No"


class CreateGoodForm:
    TITLE = "Add a good"

    class Description:
        TITLE = "Description of good"
        DESCRIPTION = "This can make it easier to find your good later"

    class IsControlled:
        TITLE = "Is your good controlled?"
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know"
        GET_CONTROL_CODE = "If you don't know you can use " + PERMISSION_FINDER_LINK

    class ControlListEntry:
        TITLE = "What's your good's control list entry?"
        DESCRIPTION = (
            "<noscript>If your good is controlled, enter its control list entry. </noscript>For example, " "ML1a. "
        )

    class Incorporated:
        TITLE = "Is your good intended to be incorporated into an end product?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"

    class PartNumber:
        TITLE = "Part Number"


class CLCQuery:
    TITLE = "Create a CLC query"
    DESCRIPTION = "By submitting you are creating a CLC query that cannot be altered"
    BACK_LINK = "Back to good"

    class CLCCode:
        TITLE = "What do you think is your good's control list entry?"
        DESCRIPTION = "For example, ML1a."

    class Additional:
        TITLE = "Further details about your goods"
        DESCRIPTION = "Please enter details of why you don't know if your good is controlled"
