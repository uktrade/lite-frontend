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
