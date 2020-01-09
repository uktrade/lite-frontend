from lite_content.lite_exporter_frontend.strings import PERMISSION_FINDER_LINK


class CreateGoodsTypeForm:
    TITLE = "Add a new product to your application"

    class Description:
        TITLE = "Description"
        DESCRIPTION = "Include the product name to make it easier to find the product when needed."

    class IsControlled:
        TITLE = "Are the products controlled??"
        DESCRIPTION = (
            "Products that aren't on the "
            + PERMISSION_FINDER_LINK
            + " may be affected by military end use controls, current trade sanctions and embargoes or weapons of "
              "mass destruction controls. If your products aren't subject to any controls, you'll get a no licence "
              "required (NLR) document from ECJU."
        )
        YES = "Yes"
        NO = "No"

    class IsIncorporated:
        TITLE = "Will the products be incorporated into other products?"
        DESCRIPTION = ""
        YES = "Yes"
        NO = "No"
