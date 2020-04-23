class Declaration:
    BACK = "Back to application summary"
    TITLE = "Declaration"
    PARAGRAPH_ONE = (
        "It’s an offence to make any statement or furnish any document or information which, "
        "to your knowledge, is false in a material particular; or recklessly make any statement or "
        "furnish any document or information which is false in a material particular. "
    )
    PARAGRAPH_TWO = (
        "A licensee must comply with the licence conditions even, where relevant, after completing the "
        "activity authorised by the licence. Failure to do so is an offence. "
    )
    PARAGRAPH_THREE = (
        "By completing and submitting this application, you agree that information provided by you, "
        "or any individual authorised to do so on behalf of your company or organisation, may be passed "
        "to international organisations or other governments in accordance with commitments entered "
        "into by Her Majesty's Government. "
    )
    PARAGRAPH_FOUR = (
        "Furthermore, any information you provide in this application may be made public under the "
        "Freedom of Information Act (FOIA) 2000. If you consider that the disclosure of any such "
        "information would be harmful to your interests please tick the box and provide a full "
        "explanation below. Please note that while the Export Control Joint Unit (ECJU) will take "
        "your views into account we cannot guarantee that the information will not be disclosed in "
        "compliance with FOIA. "
    )
    BUTTON_TITLE = "Save and continue"
    RADIO_TITLE = "Please confirm that you’ve read the terms and conditions of the licence for which you are applying."
    AGREE_TO_DECLARATION = "I have read and agreed to the terms and conditions of the licence I am applying for"


class FOI:
    TITLE = "Do you agree to FOI?"
    AGREE_TO_FOI = "Yes"
    DISAGREE_TO_FOI = "No"


class TermsAndConditions:
    TITLE = "Terms and Conditions"
    PARAGRAPH_ONE = (
        "The conditions listed here are applicable to the licence you are applying "
        "for. Further conditions may apply to the licence, or to a particular goods or "
        "destinations on the licence, once your application has been reviewed."
    )
    PARAGRAPH_TWO = (
        "If the conditions of the licence you are applying for are updated before "
        "your licence is issued, the conditions that will apply to your licence will "
        "be those that are correct at the time of the licence being issued. "
    )


class LicenceConditions:
    TITLE = "Licence Conditions"

    class Authorisation:
        TITLE = "Authorisation"
        PARAGRAPH_ONE = (
            "The Secretary of State, in exercise of powers conferred under article 26 of the Export "
            "Control Order 2008, authorises the person named in box 1 of this licence ( the licensee ) to "
            "export or transfer the goods, software and/or technology described in the attached Schedule "
            "( listed items ) to either: "
        )
        OPTION_A = "any offshore installation in a United Kingdom designated area of the Continental Shelf; or"
        OPTION_B = "any place on the high seas within a United Kingdom designated area of the Continental Shelf"
        PARAGRAPH_TWO = (
            "within a period ending on the date shown in box 3 of this licence, subject to the conditions "
            "attached or specified in this licence. "
        )

    class Conditions:
        TITLE = "Conditions"
        LIST_ITEM_ONE = (
            "This condition applies if listed items are being exported from the United Kingdom. The "
            "licensee must quote the number of this licence to the proper officer of HM Revenue and "
            "Customs when the listed items are presented to that officer for export or must comply with "
            "such alternative arrangements as are agreed with that officer."
        )
        LIST_ITEM_TWO = (
            "This condition applies if listed items are being exported or transferred from a member state "
            "of the European Community other than the United Kingdom. The licensee must present a hard "
            "copy of this licence, which has been electronically signed by an official of the Department "
            "for Business, Innovation and Skills, to the appropriate authorities in that member state on "
            "request. "
        )
        LIST_ITEM_THREE = "Items shall not be exported or transferred under this licence:"
        LIST_ITEM_THREE_A = (
            "if the exporter or transferor has been informed by a competent authority that the items "
            "are or may be intended, in their entirety or in part, for a use other than a permitted "
            "use;"
        )
        LIST_ITEM_THREE_B = (
            "if the exporter or transferor knows that the items are intended, in their entirety or in "
            "part, for a use other than a permitted use; or "
        )
        LIST_ITEM_THREE_C = (
            "if the exporter or transferor has grounds for suspecting that the items might be used, "
            "in their entirety or in part, for a use other than a permitted use, unless he has made "
            "all reasonable enquiries as to their proposed use and satisfied himself that they will "
            "not be so used. "
        )
        LIST_ITEM_FOUR = (
            "The licensee shall maintain records of all items exported or transferred under this licence "
            "(including copies of documents relating to all shipments) for at least 3 years from the end "
            "of the calendar year in which the export or transfer took place and permit them to be "
            "inspected and copied by any person authorised by the Secretary of State or the "
            "Commissioners."
        )
        LIST_ITEM_FIVE = "In this licence:"
        LIST_ITEM_FIVE_A = (
            "offshore installation has the meaning in regulation 3 of the Offshore Installation and "
            "Pipeline Works (Management and Administration) Regulations 1995 (S.I. 1995/738); "
        )
        LIST_ITEM_FIVE_B = "permitted destination in relation to an item means:"
        LIST_ITEM_FIVE_B_I = "the United Kingdom; or"
        LIST_ITEM_FIVE_B_II = (
            "any destination to which the item could be exported or transferred from the United "
            "Kingdom without an export licence; "
        )
        LIST_ITEM_FIVE_C = "permitted use means:"
        LIST_ITEM_FIVE_C_I = (
            "use on a vessel or offshore installation in connection with the operation or "
            "maintenance of an offshore installation; "
        )
        LIST_ITEM_FIVE_C_II = "onward supply, delivery or transmission to a permitted destination; or"
        LIST_ITEM_FIVE_C_III = (
            "onward supply, delivery or transmission that is in compliance with an export licence "
            "or other authorisation granted by the Secretary of State; "
        )
        LIST_ITEM_FIVE_D = (
            "United Kingdom designated area of the Continental Shelf means an area designated under "
            "section 1(7) of the Continental Shelf Act 1964 (1964 c.29). "
        )
        LIST_ITEM_SIX = (
            "The licensee must ensure SPIRE is updated, under 'Open licensing returns', with all exports "
            "except of 'technology' carried out under this licence. Details must include the licence "
            "reference, destination and end user type. This may be done at the time of each export, "
            "or at least every calendar year. "
        )
        LIST_ITEM_SEVEN = (
            "For all physical exports of items, software or technology, the licensee must ensure that "
            "the accompanying commercial documentation includes a declaration stating the ECJU "
            "reference (in the form of GBOIE20XX/XXXXX)"
        )

    class StandardConditions:
        TITLE = "Standard conditions"
        BULLET_POINTS = [
            "This licence shall not affect a prohibition or restriction in any legislation other than the legislation "
            "under which this licence was issued.",
            "This licence is not transferable.",
            "This licence may be modified or revoked at any time by the Secretary of State.",
            "This licence is valid when printed only if electronically signed by an official of the Department for "
            "Business, Innovation and Skills. ",
        ]

    class GeneralNotes:
        TITLE = "General Notes"
        LINK_TEXT = "Details of any change to export control legislation can be found at "
        LINK = "https://www.gov.uk/guidance/uk-strategic-export-control-lists-the-consolidated-list-of-strategic-military-and-dual-use-items"
        PARAGRAPH_ONE = (
            "The box numbers used on the licence form follow those in the model annexed to Council "
            "Regulation (EC) No. 428/2009. "
        )
        PARAGRAPH_TWO = (
            "Unless the context otherwise requires, any expression used in this licence shall have the "
            "meaning it bears in the Export Control Order 2008. However, the definition of 'transfer' in "
            "that Order shall apply as if for the words 'except in articles 10 and 11' to the end of the "
            "definition there were substituted the words 'or a Member State of the European Community "
            "specified as a country of origin in box 8 of this licence'. "
        )
        PARAGRAPH_THREE = (
            "**Warning:** Failure to comply with any conditions attaching to this licence may lead to forfeiture of "
            "the goods and/or to prosecution under the Customs and Excise Management Act 1979, "
            "or the legislation under which this licence was issued. "
        )
