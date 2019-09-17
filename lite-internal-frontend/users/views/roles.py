from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from core.builtins.custom_tags import get_string
from users.forms.roles import add_role, edit_role
from users.services import get_roles, get_permissions, get_role, put_role, post_role


class Roles(TemplateView):
    def get(self, request, **kwargs):
        roles, _ = get_roles(request)
        all_permissions, _ = get_permissions(request)

        context = {
            'all_permissions': all_permissions['permissions'],
            'roles': roles['roles'],
            'title': get_string('roles.title'),
        }
        return render(request, 'users/roles.html', context)


class AddRole(TemplateView):
    def get(self, request, **kwargs):
        form = add_role(request)
        return form_page(request, form)

    def post(self, request, **kwargs):
        data = {
            'name': request.POST['name'],
            'permissions': request.POST.getlist('permissions'),
        }

        response, data = submit_single_form(request,
                                            add_role(request),
                                            post_role,
                                            override_data=data)

        if response:
            return response

        return redirect(reverse('users:roles'))


class EditRole(TemplateView):
    def get(self, request, **kwargs):
        role_id = kwargs['pk']
        role, _ = get_role(request, role_id)

        return form_page(request, edit_role(request), data=role['role'])

    def post(self, request, **kwargs):
        role_id = kwargs['pk']

        data = {
            'name': request.POST['name'],
            'permissions': request.POST.getlist('permissions'),
        }

        response, data = submit_single_form(request,
                                            edit_role(request),
                                            put_role,
                                            pk=role_id,
                                            override_data=data)

        if response:
            return response

        return redirect(reverse('users:roles'))
