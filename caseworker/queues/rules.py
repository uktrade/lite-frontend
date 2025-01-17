import rules

from caseworker.advice.constants import BULK_APPROVE_ALLOWED_QUEUES


@rules.predicate
def can_user_bulk_approve_cases(request, queue_id):
    return str(queue_id) in BULK_APPROVE_ALLOWED_QUEUES


rules.add_rule("can_user_bulk_approve_cases", can_user_bulk_approve_cases)
