from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from goods import forms
from goods.services import get_goods, post_goods


class Goods(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_goods(request)

        context = {
          'data': data,
          'title': 'Manage Goods',
        }
        return render(request, 'goods/index.html', context)


class AddGood(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add Good',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = post_goods(request, request.POST)

        if status_code == 400:
            context = {
                'title': 'Add Good',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect('/goods/')
