from departments.services import get_department, get_departments, \
    post_departments, update_department
from departments import forms

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class DepartmentsList(TemplateView):

    def get(self, request, **kwargs):
        data, status_code = get_departments(request)
        context = {
            'data': data,
            'title': 'Departments',
        }
        return render(request, 'departments/index.html', context)


class AddDepartment(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add Department',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = post_departments(request, request.POST)

        if status_code == 400:
            context = {
                'title': 'Add Department',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('departments:departments'))


class EditDepartment(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_department(request, str(kwargs['pk']))
        context = {
            'data': data.get('department'),
            'title': 'Edit Department',
            'page': forms.edit_form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = update_department(request, str(kwargs['pk']), request.POST)
        if status_code == 400:
            context = {
                'title': 'Add Department',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('departments:departments'))
