import dateparser
import rules

from datetime import datetime

from exporter.applications.constants import ApplicationStatus
from exporter.goods.constants import GoodStatus


@rules.predicate
def is_application_finalised(request, application):
    if not application:
        return False

    return application.status == ApplicationStatus.FINALISED


@rules.predicate
def is_application_refused(request, application):
    if not application:
        return False

    return not application.licence


@rules.predicate
def appeal_within_deadline(request, application):
    if not application:
        return False

    if not application.appeal_deadline:
        return False

    appeal_deadline = dateparser.parse(application.appeal_deadline)
    return appeal_deadline.date() >= datetime.today().date()


@rules.predicate
def is_application_appealed(request, application):
    if not application:
        return False

    return bool(application.appeal)


@rules.predicate
def is_application_in_draft(request, application):
    return application and application.status == ApplicationStatus.DRAFT


@rules.predicate
def is_application_in_major_edit(request, application):
    return application and application.status == ApplicationStatus.APPLICANT_EDITING


rules.add_rule(
    "can_user_appeal_case",
    is_application_finalised & is_application_refused & appeal_within_deadline & ~is_application_appealed,  # noqa
)

rules.add_rule(
    "can_view_appeal_details",
    is_application_refused & is_application_appealed,
)

rules.add_rule("can_edit_quantity_value", is_application_in_draft | is_application_in_major_edit)  # noqa


# Rules for Goods
# TODO: Move to rules.py under goods/


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
