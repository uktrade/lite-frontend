from django.shortcuts import redirect
from django.urls import reverse


class ProtectAllViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != '/login/':
            return redirect(reverse('core:login'))

        response = self.get_response(request)

        return response
