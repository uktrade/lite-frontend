from caseworker.queues.services import get_queue


class RequestQueueMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_kwargs.get("queue_pk"):
            request.queue = get_queue(request, view_kwargs["queue_pk"])
