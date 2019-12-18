class GoodsList:
    TITLE = "Products"
    CREATE_GOOD = "Add a product"

    ORGANISATION_NO_GOODS = "Your organisation doesn't have any products."
    FILTERED_NO_GOODS = "There are no products based on filter"
    ORGANISATION_GOODS = "Your organisation has %s products"  # %s reference the count of goods
    FILTERED_GOODS = "Displaying %s products"  # %s reference the count of goods

    class Filter:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list entry"
        PART_NUMBER = "Part number"
        APPLY = "Apply filters"
        CLEAR = "Clear filters"
        SHOW = "Show filters"
        HIDE = "Hide filters"

    class Table:
        DESCRIPTION = "Description"
        CONTROL_LIST_ENTRY = "Control list entry"
        PART_NUMBER = "Part number"
        STATUS = "Status"
