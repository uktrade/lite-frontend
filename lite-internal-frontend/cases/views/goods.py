from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from cases.forms.review_goods_clc import review_goods_clc_query_form
from cases.services import get_good, get_case, post_goods_control_code
from core.builtins.custom_tags import get_string
from core.helpers import convert_dict_to_query_params


class Good(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        good_pk = str(kwargs['good_pk'])
        good, _ = get_good(request, good_pk)

        context = {
            'case': {'id': case_id},
            'good': good['good']
        }
        return render(request, 'cases/case/good.html', context)


class ReviewGoods(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])

        action = request.GET.get('action')
        if action == 'edit-flags':
            params = dict()
            params['goods'] = request.GET.getlist('goods')
            params['level'] = 'goods'
            post_url = '?' + convert_dict_to_query_params(params)
            return redirect(reverse_lazy('cases:assign_flags', kwargs={'pk': case_id}) + post_url)

        goods_pk_list = request.GET.getlist('items', request.GET.getlist('goods'))
        goods = []

        if not goods_pk_list:
            return redirect(reverse_lazy('cases:case', kwargs={'pk': case_id}))

        case = get_case(request, case_id)

        edit_flags_url = reverse_lazy('cases:assign_flags', kwargs={'pk': case_id})
        review_goods_clc_url = reverse_lazy('cases:review_goods_clc', kwargs={'pk': case_id})
        parameters = {
            'level': 'goods',
            'origin': 'review_goods',
            'goods': goods_pk_list
        }
        goods_postfix_url = '?' + convert_dict_to_query_params(parameters)

        for good in case['application']['goods']:
            if good['good']['id'] in goods_pk_list:
                goods.append(good)

        context = {
            'title': get_string('cases.review_goods_summary.heading'),
            'case_id': case_id,
            'objects': goods,
            'edit_flags_url': edit_flags_url + goods_postfix_url,
            'review_goods_clc_url': review_goods_clc_url + goods_postfix_url
        }
        return render(request, 'cases/case/review-goods.html', context)


class ReviewGoodsClc(TemplateView):
    case_id = None
    goods = None
    back_link = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        self.goods = request.GET.getlist('items', request.GET.getlist('goods'))

        parameters = {
            'goods': self.goods
        }
        goods_postfix_url = "?" + convert_dict_to_query_params(parameters)

        self.back_link = reverse_lazy('cases:review_goods', kwargs={'pk': self.case_id}) + goods_postfix_url

        return super(ReviewGoodsClc, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = review_goods_clc_query_form(request, self.back_link)
        if len(self.goods) == 1:
            data = get_good(request, self.goods[0])[0]['good']
        else:
            initial_good = get_good(request, self.goods[0])[0]['good']
            for good in self.goods[1:]:
                good_data = get_good(request, good)[0]['good']
                if initial_good['control_code'] != good_data['control_code'] \
                    and initial_good['is_good_controlled'] != good_data['is_good_controlled'] \
                        and initial_good['comment'] != good_data['comment'] \
                        and initial_good['report_summary'] != good_data['report_summary']:
                    return form_page(request, form)
            data = initial_good
        return form_page(request, form, data=data)

    def post(self, request, *args, **kwargs):
        form_data = {
            'objects': self.goods,
            'comment': request.POST.get('comment'),
            'report_summary': request.POST.get('report_summary'),
            'control_code': request.POST.get('control_code', None),
            'is_good_controlled': request.POST.get('is_good_controlled')
        }

        if request.POST.get('report_summary') == 'None':
            del form_data['report_summary']

        response = post_goods_control_code(request, self.case_id, form_data)

        if response.status_code == 400:
            form = review_goods_clc_query_form(request, self.back_link)
            return form_page(request, form, data=request.POST, errors=response.json().get('errors'))

        return redirect(self.back_link)
