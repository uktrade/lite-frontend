from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from goodstype import forms
from goodstype.services import post_goods_type, get_goods_type


class GoodsType(TemplateView):
    def get(self, request, pk):
        data, _ = get_goods_type(request, pk)

        context = {
            'data': data,
            'title': 'Manage GoodsTypes',
        }
        return render(request, 'goodstype/index.html', context)


class AddGoodsType(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.form)

    def post(self, request, **kwargs):
        copied_post = request.POST.copy()
        copied_post['content_type'] = 'draft'
        copied_post['object_id'] = kwargs.get('pk')
        data, status_code = post_goods_type(request, copied_post)

        if status_code == 400:
            return form_page(request, forms.form, request.POST, errors=data['errors'])

        return redirect(reverse_lazy('goods:goods'))


class DraftAddGoodsType(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.form)

    def post(self, request, **kwargs):
        copied_post = request.POST.copy()
        copied_post['content_type'] = 'draft'
        copied_post['object_id'] = str(kwargs.get('pk'))
        data, status_code = post_goods_type(request, copied_post)

        if status_code == 400:
            return form_page(request, forms.form, request.POST, errors=data['errors'])

        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect(reverse_lazy('apply_for_a_licence:overview', args=[kwargs['pk']]))