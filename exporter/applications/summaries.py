from core.summaries.reducers import firearm_reducer


def firearm_product_summary(good, is_user_rfd, organisation_documents):
    return firearm_reducer(good, is_user_rfd, organisation_documents)
