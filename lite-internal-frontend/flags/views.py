from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.builtins.custom_tags import get_string
from flags.forms import add_flag_form, edit_flag_form
from flags.services import get_flags, post_flags, get_flag, put_flag
from libraries.forms.generators import form_page
from users.services import get_gov_user


class FlagsList(TemplateView):

    def get(self, request, **kwargs):
        data, status_code = get_flags(request)
        user_data, status_code = get_gov_user(request, str(request.user.user_token))

        try:
            status = kwargs['status']
        except KeyError:
            status = 'active'

        if status == 'active':
            status = 'no_deactivated'
            flags = []
            for flag in data['flags']:
                if flag['status'] == 'Deactivated':
                    status = 'active'
                if flag['status'] == 'Active':
                    flags.append(flag)
            data['flags'] = flags

        context = {
            'data': data,
            'status': status,
            'title': 'Flags',
            'user_data': user_data,
        }
        return render(request, 'flags/index.html', context)


class AddFlag(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, add_flag_form())

    def post(self, request, **kwargs):
        response, status_code = post_flags(request, request.POST)
        if status_code != 201:
            return form_page(request, add_flag_form(), data=request.POST, errors=response.get('errors'))

        return redirect(reverse_lazy('flags:flags'))


class EditFlag(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_flag(request, str(kwargs['pk']))
        return form_page(request, edit_flag_form(), data=data['flag'])

    def post(self, request, **kwargs):
        response, status_code = put_flag(request, str(kwargs['pk']), request.POST)
        if status_code != 200:
            return form_page(request, edit_flag_form(), data=request.POST, errors=response.get('errors'))

        return redirect(reverse_lazy('flags:flags'))


class ViewFlag(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_flag(request, str(kwargs['pk']))

        context = {
            'data': data,
            'title': data['flag']['name']
        }
        return render(request, 'flags/profile.html', context)


class ChangeFlagStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs['status']
        description = ''

        if status != 'deactivate' and status != 'reactivate':
            raise Http404

        if status == 'deactivate':
            description = get_string('flags.update_flag.status.deactivate_warning')

        if status == 'reactivate':
            description = get_string('flags.update_flag.status.reactivate_warning')

        context = {
            'title': 'Are you sure you want to {} this flag?'.format(status),
            'description': description,
            'user_id': str(kwargs['pk']),
            'status': status,
        }
        return render(request, 'flags/change_status.html', context)

    def post(self, request, **kwargs):
        status = kwargs['status']

        if status != 'deactivate' and status != 'reactivate':
            raise Http404

        put_flag(request, str(kwargs['pk']), json={'status': request.POST['status']})

        return redirect(reverse_lazy('flags:flags'))

