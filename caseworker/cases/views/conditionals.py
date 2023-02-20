from caseworker.queues.services import get_queue


def is_queue_in_url_system_queue(wizard):
    queue = get_queue(wizard.request, wizard.kwargs["queue_pk"])
    return queue["is_system_queue"]
