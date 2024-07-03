import rules

from exporter.goods.constants import GoodStatus


@rules.predicate
def is_draft_product(request, product):
    return product and product["status"]["key"] == GoodStatus.DRAFT


@rules.predicate
def is_submitted_product(request, product):
    return product and product["status"]["key"] == GoodStatus.SUBMITTED


@rules.predicate
def is_verified_product(request, product):
    return product and product["status"]["key"] == GoodStatus.VERIFIED


@rules.predicate
def is_archived_product(request, product):
    return product and product["is_archived"] is True


rules.add_rule("can_delete_product", is_draft_product)

rules.add_rule(
    "can_archive_product",
    (is_submitted_product | is_verified_product) & ~is_archived_product,  # noqa
)

rules.add_rule("can_restore_product", is_archived_product)  # noqa
