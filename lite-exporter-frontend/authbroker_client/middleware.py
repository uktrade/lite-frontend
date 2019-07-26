from django.shortcuts import redirect
from django.urls import resolve


class ProtectAllViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if resolve(request.path).app_name != 'authbroker_client' and not request.user.is_authenticated:
            return redirect('authbroker:login')

        response = self.get_response(request)

        return response
