from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.services import get_clc_notifications
from goods import forms
from goods.forms import edit_form
from goods.services import get_goods, post_goods, get_good, update_good, delete_good
from libraries.forms.components import HiddenField
from libraries.forms.generators import form_page


class Goods(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_goods(request)
        notifications, _ = get_clc_notifications(request, unviewed=True)
        notifications_ids_list = [x['clc_query'] for x in notifications['results']]

        context = {
            'data': data,
            'title': 'Manage Goods',
            'notifications_ids_list': notifications_ids_list,
        }
        return render(request, 'goods/index.html', context)


class GoodsDetail(TemplateView):
    def get(self, request, **kwargs):
        good_id = kwargs['pk']
        data, status_code = get_good(request, str(good_id))

        visible_notes = filter(lambda note: note['is_visible_to_exporter'], data['good']['notes'])

        context = {
            'data': data,
            'notes': visible_notes,
            'title': data['good']['description'],
        }

        return render(request, 'goods/good.html', context)


class AddGood(TemplateView):
    main_form = forms.add_goods_questions

    def get(self, request, **kwargs):
        return form_page(request, self.main_form)

    def post(self, request):
        data = request.POST.copy()

        # Logic for when we are at the confirmation page
        data['validate_only'] = False

        if 'clc_query_confirmation' in data:
            if data['is_good_controlled'] == 'unsure' and data['clc_query_confirmation'] == 'yes':
                data['are_you_sure'] = True
                data['control_code'] = data['not_sure_details_control_code']
                data, status_code = post_goods(request, data)
                if status_code == 400:
                    return form_page(request, self.main_form, request.POST, errors=data['errors'])

                return redirect(reverse_lazy('goods:goods'))
            elif data['is_good_controlled'] == 'unsure' and data['clc_query_confirmation'] == 'no':
                # user answered no on confirmation page and return to goods list
                return redirect(reverse_lazy('goods:goods'))

        # On first page - validate without saving to see if we should head for confirmation page
        data['validate_only'] = True
        validated_data, status_code = post_goods(request, data)

        if 'errors' in validated_data and validated_data['errors']:
            return form_page(request, self.main_form, data=data, errors=validated_data.get('errors'))

        data['validate_only'] = False

        # on first page for unsure good and no errors - put all data from first form in hidden fields and direct to
        # confirmation page
        if 'is_good_controlled' in data and data['is_good_controlled'] == 'unsure':
            are_you_sure_form = forms.are_you_sure
            for key, value in data.items():
                are_you_sure_form.questions.append(
                    HiddenField(key, value)
                )
            return form_page(request, are_you_sure_form)

        # User has clicked submit with controlled good being yes or no
        validated_data, status_code = post_goods(request, data)

        if 'errors' in validated_data:
            if validated_data['errors']:
                return form_page(request, self.main_form, data=data, errors=validated_data.get('errors'))

        return redirect(reverse_lazy('goods:goods'))


class DraftAddGood(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.form)

    def post(self, request, **kwargs):
        data, status_code = post_goods(request, request.POST)

        if status_code == 400:
            return form_page(request, forms.form, request.POST, errors=data['errors'])

        return redirect(reverse_lazy('apply_for_a_licence:overview'), kwargs['pk'])


class EditGood(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_good(request, str(kwargs['pk']))
        return form_page(request, edit_form, data['good'])

    def post(self, request, **kwargs):
        data, status_code = update_good(request, str(kwargs['pk']), request.POST)

        if status_code == 400:
            return form_page(request, edit_form, request.POST, errors=data['errors'])

        return redirect(reverse_lazy('goods:goods'))


class DeleteGood(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_good(request, str(kwargs['pk']))
        if data['good']['status'] != 'draft':
            context = {
                'title': 'Cannot Delete Good',
                'description': 'This good is already inside a application',
                'flag': 'cannot_delete',
            }
        else:
            context = {
                'good': data['good'],
                'title': 'Delete Good',
                'description': 'Are you sure you want to delete this good?',
                'flag': 'can_delete',
            }
        return render(request, 'goods/confirm_delete.html', context)

    def post(self, request, **kwargs):
        delete_good(request, str(kwargs['pk']))
        return redirect(reverse_lazy('goods:goods'))
