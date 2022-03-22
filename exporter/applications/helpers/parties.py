from exporter.core.constants import FirearmsProductType


def party_requires_ec3_document(application):
    """
    Helper function to determine EC3 document requirement status for End-user

    We only need to ask if the goods originate from NI, going to EU and the
    product type is not software or technology related to firearms. If we have
    atleast one other type included then we need to ask for this form provided
    the other conditions satisfy.
    Since the user may not have added the products before entering End-user details
    and vice versa this needs checking in multiple places and accodingly notify user.
    """

    # user may not have completed the goods location section
    goods_from_NI = application.get("goods_starting_point", "") == "NI"

    # user may not have entered end-user details yet
    eu_destination = False
    destination = application.get("destinations", {})
    if (
        destination
        and destination["type"] == "end_user"
        and destination["data"]
        and destination["data"]["country"]["is_eu"]
    ):
        eu_destination = True

    ec3_product_types = {
        FirearmsProductType.FIREARMS,
        FirearmsProductType.AMMUNITION,
        FirearmsProductType.COMPONENTS_FOR_FIREARMS,
        FirearmsProductType.COMPONENTS_FOR_AMMUNITION,
        FirearmsProductType.FIREARMS_ACCESSORY,
    }
    product_types = {
        product["firearm_details"]["type"]["key"]
        for product in application.get("goods", [])
        if product.get("firearm_details")
    }
    firearms_products = ec3_product_types.intersection(product_types)

    return goods_from_NI and eu_destination and firearms_products
