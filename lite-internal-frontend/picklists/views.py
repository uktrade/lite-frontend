from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from libraries.forms.generators import form_page
from picklists.forms import add_picklist_item_form, edit_picklist_item_form, deactivate_picklist_item, \
    reactivate_picklist_item
from picklists.services import get_picklists, get_picklist_item, post_picklist_item, put_picklist_item
from teams.services import get_team
from users.services import get_gov_user


class Picklists(TemplateView):

    def get(self, request, **kwargs):
        """
        Return a list of picklists and show all the relevant items
        """
        # Ensure that the page has a type
        picklist_type = request.GET.get('type')
        if not picklist_type:
            return redirect(reverse_lazy('picklists:picklists') + '?type=proviso')
        user, status_code = get_gov_user(request)
        team, status_code = get_team(request, user['user']['team']['id'])
        picklist_items, status_code = get_picklists(request, picklist_type, True)

        active_picklist_items = [x for x in picklist_items['picklist_items'] if x['status']['key'] == 'active']
        deactivated_picklist_items = [x for x in picklist_items['picklist_items'] if x['status']['key'] != 'active']

        context = {
            'title': 'Picklists - ' + team['team']['name'],
            'team': team['team'],
            'active_picklist_items': active_picklist_items,
            'deactivated_picklist_items': deactivated_picklist_items,
            'type': picklist_type,
        }
        return render(request, 'teams/picklist.html', context)


class AddPicklistItem(TemplateView):
    def get(self, request, **kwargs):
        picklist_type = request.GET.get('type')

        data = {
            'type': picklist_type
        }

        return form_page(request, add_picklist_item_form(), data=data)

    def post(self, request, **kwargs):
        response, status_code = post_picklist_item(request, request.POST)

        if status_code != 201:
            return form_page(request, add_picklist_item_form(), data=request.POST, errors=response.get('errors'))

        picklist_type = request.POST['type']

        return redirect(reverse_lazy('picklists:picklists') + '?type=' + picklist_type)


class ViewPicklistItem(TemplateView):
    def get(self, request, **kwargs):
        picklist_item, status_code = get_picklist_item(request, str(kwargs['pk']))

        context = {
            'title': picklist_item['picklist_item']['name'],
            'picklist_item': picklist_item['picklist_item'],
        }
        return render(request, 'teams/picklist-item.html', context)


class EditPicklistItem(TemplateView):
    picklist_item_id = None
    picklist_item = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.picklist_item_id = str(kwargs['pk'])
        self.picklist_item, status_code = get_picklist_item(request, self.picklist_item_id)
        self.form = edit_picklist_item_form(self.picklist_item)

        return super(EditPicklistItem, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=self.picklist_item['picklist_item'])

    def post(self, request, **kwargs):
        response, status_code = put_picklist_item(request, self.picklist_item_id, request.POST)

        if status_code != 200:
            return form_page(request, self.form, data=request.POST, errors=response.get('errors'))

        return redirect(reverse_lazy('picklists:picklist_item', kwargs={'pk': response['picklist_item']['id']}))


class DeactivatePicklistItem(TemplateView):
    picklist_item_id = None
    picklist_item = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.picklist_item_id = str(kwargs['pk'])
        self.picklist_item, status_code = get_picklist_item(request, self.picklist_item_id)
        self.form = deactivate_picklist_item(self.picklist_item)

        return super(DeactivatePicklistItem, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        if self.picklist_item['picklist_item']['status']['key'] == 'deactivated':
            raise Http404

        return form_page(request, self.form)

    def post(self, request, **kwargs):
        data = {
            'status': 'deactivated'
        }

        put_picklist_item(request, self.picklist_item_id, data)
        return redirect(reverse_lazy('picklists:picklist_item', kwargs={'pk': self.picklist_item['picklist_item']['id']}))


class ReactivatePicklistItem(TemplateView):
    picklist_item_id = None
    picklist_item = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.picklist_item_id = str(kwargs['pk'])
        self.picklist_item, status_code = get_picklist_item(request, self.picklist_item_id)
        self.form = reactivate_picklist_item(self.picklist_item)

        return super(ReactivatePicklistItem, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        if self.picklist_item['picklist_item']['status']['key'] != 'deactivated':
            raise Http404

        return form_page(request, self.form)

    def post(self, request, **kwargs):
        data = {
            'status': 'active'
        }

        put_picklist_item(request, self.picklist_item_id, data)
        return redirect(reverse_lazy('picklists:picklist_item', kwargs={'pk': self.picklist_item['picklist_item']['id']}))
