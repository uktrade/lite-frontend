from caseworker.users.services import get_gov_user


class RequestUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if "lite_api_user_id" not in request.session:
            return
        response_data, status_code = get_gov_user(request, str(request.session["lite_api_user_id"]))
        if not status_code == 200:
            return
        request.user = response_data.get("user", None)
