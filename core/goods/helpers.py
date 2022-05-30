from core.goods.constants import FIREARM_CATEGORIES_MADE_BEFORE_1938


def is_product_category_made_before_1938(firearm_details):
    firearm_categories = firearm_details["category"]
    for firearm_category in firearm_categories:
        if firearm_category["key"] in FIREARM_CATEGORIES_MADE_BEFORE_1938:
            return True

    return False
