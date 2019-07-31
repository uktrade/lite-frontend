from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.builtins.custom_tags import get_string
from core.helpers import Section, Tile, generate_notification_string
from core.services import get_notifications, get_clc_notifications
from users.services import get_user


class Hub(TemplateView):
    def get(self, request, **kwargs):
        user, _status_code = get_user(request)
        response, _ = get_notifications(request, unviewed=True)
        num_notifications = response['count']
        response, _ = get_clc_notifications(request, unviewed=True)
        num_clc_notifications = response['count']

        context = {
            'title': get_string('hub.title'),
            'sections': [
                Section('', '', [
                    Tile(get_string('licences.apply_for_a_licence'), '',
                         reverse_lazy('apply_for_a_licence:index')),
                ]),
                Section('Manage', '', [
                    Tile(get_string('drafts.title'), '',
                         reverse_lazy('drafts:drafts')),
                    Tile(get_string('applications.title'), generate_notification_string(num_notifications),
                         reverse_lazy('applications:applications')),
                    Tile('Goods', generate_notification_string(num_clc_notifications),
                         reverse_lazy('goods:goods')),
                    Tile('Sites', '', reverse_lazy('sites:sites')),
                    Tile('Users', '', reverse_lazy('users:users')),
                ]),
            ],
            'applicationDeleted': request.GET.get('application_deleted'),
            'organisation': user['user']['organisation'],
        }
        return render(request, 'core/hub.html', context)
