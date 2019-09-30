from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from core.builtins.custom_tags import get_string
from core.forms import select_your_organisation_form
from core.helpers import Section, Tile, generate_notification_string
from core.services import get_notifications, get_organisation
from users.services import get_user


class Hub(TemplateView):
    def get(self, request, **kwargs):
        user, _ = get_user(request)

        notifications = get_notifications(request, unviewed=True)
        organisation = get_organisation(request, str(request.user.organisation))
        sections = [
                Section('', [
                    Tile(get_string('licences.apply_for_a_licence'), '',
                         reverse_lazy('apply_for_a_licence:index')),
                ]),
                Section('Manage', [
                    Tile(get_string('drafts.title'), '',
                         reverse_lazy('drafts:drafts')),
                    Tile(get_string('applications.title'), generate_notification_string(notifications, 'application'),
                         reverse_lazy('applications:applications')),
                    Tile('Goods', generate_notification_string(notifications, 'control_list_classification_query'),
                         reverse_lazy('goods:goods')),
                    Tile('End User Advisories', generate_notification_string(notifications, 'end_user_advisory_query'),
                         reverse_lazy('end_users:end_users')),
                ]),
            ]

        if organisation.get('sub_type').get('key') == 'individual':
            sections[1].tiles.append(Tile('Manage my sites', '', reverse_lazy('sites:sites')))
        else:
            sections[1].tiles.append(Tile('Manage my organisation', '', reverse_lazy('users:users')))

        context = {
            'organisation': organisation,
            'sections': sections,
            'application_deleted': request.GET.get('application_deleted'),
            'user_data': user['user'],
            'notifications': notifications
        }

        return render(request, 'core/hub.html', context)


class PickOrganisation(TemplateView):
    form = None
    organisations = None

    def dispatch(self, request, *args, **kwargs):
        user, _ = get_user(request)
        self.organisations = user['user']['organisations']
        self.form = select_your_organisation_form(self.organisations)

        if len(self.organisations) == 1:
            raise Http404()

        return super(PickOrganisation, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        data = {
            'organisation': str(request.user.organisation)
        }

        return form_page(request, self.form, data=data)

    def post(self, request, **kwargs):
        # If no data is given, error
        if not request.POST.get('organisation'):
            return form_page(request, self.form, errors={'organisation': ['Select an organisation to use']})

        request.user.organisation = request.POST['organisation']
        request.user.save()

        return redirect('/')
