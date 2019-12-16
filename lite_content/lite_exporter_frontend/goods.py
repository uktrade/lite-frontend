from .strings import PERMISSION_FINDER_LINK


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
    BUTTON = "Save"

    class Description:
        TITLE = "Description of good"
        DESCRIPTION = "This can make it easier to find your good later"

    class IsControlled:
        TITLE = "Is your good controlled?"
        DESCRIPTION = "If you don't know you can use " + PERMISSION_FINDER_LINK
        CLC_REQUIRED = (
            "Goods that aren't on the "
            + PERMISSION_FINDER_LINK
            + "may be affected by military end use controls, current trade sanctions and embargoes or weapons of mass "
            + "destruction controls. If your goods and services aren't subject to any controls, you'll get a no "
            + "licence required (NLR) document from ECJU. "
        )
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know"

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


class CLCQueryForm:
    TITLE = "Create a CLC query"
    DESCRIPTION = "By submitting you are creating a CLC query that cannot be altered"
    BACK_LINK = "Back to good"
    BUTTON = "Save"

    class CLCCode:
        TITLE = "What do you think is your good's control list entry?"
        DESCRIPTION = "For example, ML1a."

    class Additional:
        TITLE = "Further details about your goods"
        DESCRIPTION = "Please enter details of why you don't know if your good is controlled"


class EditGoodForm:
    TITLE = "Edit Good"
    DESCRIPTION = ""

    class Description:
        TITLE = "Description of good"
        DESCRIPTION = "This can make it easier to find your good later"

    class IsControlled:
        TITLE = "Is your good controlled?"
        DESCRIPTION = "If you don't know you can use " + PERMISSION_FINDER_LINK
        YES = "Yes"
        NO = "No"
        UNSURE = "I don't know"

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

    class Buttons:
        SAVE = "Save"
        DELETE = "Delete Good"
