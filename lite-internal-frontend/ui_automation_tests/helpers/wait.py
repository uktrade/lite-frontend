import time

# How many attempts to wait for the function to return True
timeout_limit = 20
# How frequently in seconds the function should be checked
function_retry_interval = 1


def wait_for_function(func, **kwargs):
    time_no = 0
    while time_no < timeout_limit:
        if func(**kwargs):
            return True
        time.sleep(function_retry_interval)
        time_no += function_retry_interval
    return False


def wait_for_end_user_document(api, draft_id):
    return wait_for_function(api.check_end_user_document_is_processed, draft_id=draft_id)


def wait_for_ultimate_end_user_document(api, draft_id, ultimate_end_user_id):
    return wait_for_function(api.check_ultimate_end_user_document_is_processed, draft_id=draft_id,
                             ultimate_end_user_id=ultimate_end_user_id)
