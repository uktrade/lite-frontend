from conf.constants import NOT_STARTED, IN_PROGRESS, DONE


def check_all_parties_have_a_document(parties):
    if not parties:
        return NOT_STARTED

    for party in parties:
        if not party:
            return NOT_STARTED

        if not party["document"]:
            return IN_PROGRESS

    return DONE
