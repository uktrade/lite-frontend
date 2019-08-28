from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.urls import resolve
from lite_forms.generators import error_page

from users.services import get_user


class ProtectAllViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if resolve(request.path).app_name != 'authbroker_client' and not request.user.is_authenticated:
            return redirect('authbroker:login')

        if not isinstance(request.user, AnonymousUser):
            if not request.user.organisation:
                user_dict = get_user(request)

                if len(user_dict['user']['organisations']) == 0:
                    return error_page(request, 'You don\'t belong to any organisations', show_back_link=False)
                elif len(user_dict['user']['organisations']) > 1:
                    return redirect('core:pick_organisation')
                else:
                    user = request.user
                    user.organisation = user_dict['user']['organisations'][0]['id']
                    user.save()

        response = self.get_response(request)

        return response
