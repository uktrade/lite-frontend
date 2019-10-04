from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from drafts.services import get_draft_goods_types, get_draft_countries
from goodstype.forms import goods_type_form
from goodstype.services import post_goods_type, post_goods_type_countries


class DraftAddGoodsType(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, goods_type_form())

    def post(self, request, **kwargs):
        copied_post = request.POST.copy()
        copied_post['application'] = str(kwargs.get('pk'))
        data, status_code = post_goods_type(request, copied_post)

        if status_code == 400:
            return form_page(request, goods_type_form(), request.POST, errors=data['errors'])

        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect(reverse_lazy('apply_for_a_licence:overview', args=[kwargs['pk']]))


class GoodsTypeCountries(TemplateView):
    goods = None
    countries = None
    draft_id = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs['pk'])
        goods, _ = get_draft_goods_types(request, self.draft_id)
        self.goods = goods['goods']
        countries, _ = get_draft_countries(request, self.draft_id)
        self.countries = countries['countries']

        return super(GoodsTypeCountries, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'countries': self.countries,
            'goods': self.goods,
            'draft_id': self.draft_id,
            'title': 'Explain where each item is going'
        }
        return render(request, 'apply_for_a_licence/goodstype/countries.html', context)

    def post(self, request, **kwargs):
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken')

        post_data = {}

        for good_country in data:
            split_data = good_country.split('.')
            if str(split_data[0]) not in str(post_data):
                post_data[split_data[0]] = []
            post_data[split_data[0]].append(split_data[1])

        for good in self.goods:
            if good['id'] not in str(data):
                post_data[good['id']] = []

        post_goods_type_countries(request, post_data)

        return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': self.draft_id}))
