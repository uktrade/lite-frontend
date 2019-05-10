from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from libraries.forms.helpers import nest_data, flatten_data
from sites import forms
from sites.services import get_sites, get_site, post_sites, put_site


class Sites(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_sites(request)

        context = {
            'title': 'Sites',
            'data': data,
        }
        return render(request, 'sites/index.html', context)


class NewSite(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'New Site',
            'page': forms.new_site_form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data = request.POST.copy()

        # Post the data to the validator and check for errors
        nested_data = nest_data(data)
        validated_data, status_code = post_sites(request, nested_data)

        if 'errors' in validated_data:
            context = {
                'page': forms.new_site_form,
                'title': forms.new_site_form.title,
                'errors': validated_data['errors'],
                'data': data,
            }
            return render(request, 'form.html', context)

        return redirect('/sites/')


class EditSite(TemplateView):
    def get(self, request, **kwargs):
        site, status_code = get_site(request, str(kwargs['pk']))

        context = {
            'title': 'Edit Site',
            'page': forms.edit_site_form,
            'data': flatten_data(site.get('site')),
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        validated_data, status_code = put_site(request, str(kwargs['pk']), json=nest_data(request.POST))

        if 'errors' in validated_data:
            context = {
                'title': 'Edit Site',
                'page': forms.edit_site_form,
                'data': request.POST,
                'errors': flatten_data(validated_data.get('errors')),
            }
            return render(request, 'form.html', context)

        return redirect('/sites/')
