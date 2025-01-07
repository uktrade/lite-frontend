import rules

BULK_APPROVE_ALLOWED_QUEUES = {
    "MOD_CAPPROT": "93d1bc19-979d-4ba3-a57c-b0ce253c6237",  # /PS-IGNORE
    "MOD_DI_INDIRECT": "0dd6c6f0-8f8b-4c03-b68f-0d8b04225369",  # /PS-IGNORE
    "MOD_DSR": "a84d6556-782e-4002-abe2-8bc1e5c2b162",  # /PS-IGNORE
    "MOD_DSTL": "1a5f47ee-ef5e-456b-914c-4fa629b4559c",  # /PS-IGNORE
}


@rules.predicate
def can_user_bulk_approve_cases(request, queue):
    return queue["id"] in BULK_APPROVE_ALLOWED_QUEUES.values()


rules.add_rule("can_user_bulk_approve_cases", can_user_bulk_approve_cases)
