from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.builtins.custom_tags import get_string
from libraries.forms.generators import form_page
from libraries.forms.helpers import nest_data, flatten_data
from sites.forms import new_site_form, edit_site_form
from sites.services import get_sites, get_site, post_sites, put_site


class Sites(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_sites(request)

        context = {
            'title': get_string('sites.title'),
            'data': data,
        }
        return render(request, 'sites/index.html', context)


class NewSite(TemplateView):
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.form = new_site_form()

        return super(NewSite, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        validated_data, status_code = post_sites(request, nest_data(request.POST))

        if 'errors' in validated_data:
            validated_data['errors'] = flatten_data(validated_data['errors'])
            return form_page(request, self.form, data=request.POST, errors=validated_data['errors'])

        return redirect(reverse_lazy('sites:sites'))


class EditSite(TemplateView):
    site = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.site, status_code = get_site(request, str(kwargs['pk']))
        self.form = edit_site_form('Edit ' + self.site['site']['name'])

        return super(EditSite, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=flatten_data(self.site.get('site')))

    def post(self, request, **kwargs):
        validated_data, status_code = put_site(request, str(kwargs['pk']), json=nest_data(request.POST))

        if 'errors' in validated_data:
            validated_data['errors'] = flatten_data(validated_data['errors'])
            return form_page(request, self.form, data=request.POST, errors=validated_data['errors'])

        return redirect(reverse_lazy('sites:sites'))
