from http import HTTPStatus

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from applications.forms.goods import good_on_application_form, add_new_good_forms
from applications.helpers.check_your_answers import get_total_goods_value
from applications.services import (
    get_application,
    get_application_goods,
    get_application_goods_types,
    post_good_on_application,
    delete_application_preexisting_good,
    validate_application_good,
    add_document_data,
)
from core.helpers import convert_dict_to_query_params
from core.services import get_units
from goods.services import get_goods, get_good, validate_good, post_goods, post_good_documents
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import HiddenField
from lite_forms.generators import error_page, form_page


class DraftGoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List all goods relating to the draft
        """
        draft_id = str(kwargs["pk"])
        application = get_application(request, draft_id)
        goods = get_application_goods(request, draft_id)
        goods_value = get_total_goods_value(goods)

        context = {"goods": goods, "application": application, "goods_value": goods_value}
        return render(request, "applications/goods/index.html", context)


class GoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List of existing goods  (add-preexisting)
        """
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        description = request.GET.get("description", "").strip()
        part_number = request.GET.get("part_number", "").strip()
        control_rating = request.GET.get("control_rating", "").strip()

        params = {
            "page": int(request.GET.get("page", 1)),
            "description": description,
            "part_number": part_number,
            "control_rating": control_rating,
            "for_application": "True",
        }
        goods_list = get_goods(request, **params)

        context = {
            "application": application,
            "data": goods_list,
            "description": description,
            "part_number": part_number,
            "control_code": control_rating,
            "draft_id": application_id,
            "params": params,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
        }
        return render(request, "applications/goods/preexisting.html", context)


@method_decorator(csrf_exempt, "dispatch")
class AddNewGood(TemplateView):
    title = "Add Good"
    form = None
    form_num = None
    application_id = None
    prefix = ["good_", "good_on_app_"]
    fields = [
        [
            "good_description",
            "good_control_code",
            "good_part_number",
            "good_is_good_controlled",
            "good_is_good_end_product",
        ],
        ["good_on_app_value", "good_on_app_quantity", "good_on_app_unit"],
        [],
    ]
    data = None
    errors = None
    validation_function = [validate_good, validate_application_good]

    def get(self, request, **kwargs):
        self.application_id = str(kwargs["pk"])
        self.data = {}
        self.generate_form(request, 0)
        return form_page(request, self.form, self.data, extra_data={"form_pk": self.form_num})

    @csrf_exempt
    def post(self, request, **kwargs):
        # This has to be run at the top of the method before POST is accessed.
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        self.application_id = str(kwargs["pk"])
        form_num = int(request.POST.get("form_pk"))

        if request.POST.get("_action", None) == "back":
            generate_form_num = form_num - 1
            self.data = request.POST.copy()
            del self.data["_action"]
            self.generate_form(request, generate_form_num)

        elif form_num == 0:
            self.handle_post_for_form(request, form_num)

        elif form_num == 1:
            self.handle_post_for_form(request, form_num, pk=self.application_id)

        elif form_num == 2:
            if request.FILES:
                # post good
                post_data = request.POST.copy()

                validated_data, status_code = post_goods(request, post_data)

                if status_code != HTTPStatus.CREATED:
                    raise Http404

                # attach document
                good_id = validated_data["good"]["id"]
                data, error = add_document_data(request)

                if error:
                    return error_page(request, error)

                # Send LITE API the file information
                post_good_documents(request, good_id, [data])

                # Attach good to application
                post_data["good_id"] = good_id

                post_good_on_application(request, self.application_id, post_data)

                return redirect("applications:goods", self.application_id)
            else:
                # Error is thrown if a document is not attached
                self.data = request.POST.copy()
                self.generate_form(request, form_num)
                self.errors = {"documents": [strings.goods.CreateGoodOnApplicationForm.DOCUMENT_MISSING]}

        return form_page(request, self.form, self.data, self.errors, {"form_pk": self.form_num})

    def handle_post_for_form(self, request, form_num, pk=None):
        post = request.POST.copy()
        del post["form_pk"]
        del post["_action"]

        # Call the relevant validation function for the form that posted.
        if pk:
            data = self.validation_function[form_num](request, pk, json=post)
        else:
            data = self.validation_function[form_num](request, json=post)

        if data.status_code != HTTPStatus.OK:
            self.data = post
            self.generate_form(request, form_num)
            self.errors = self.add_prefix_to_errors(data.json()["errors"], self.prefix[form_num])
        else:
            self.data = post
            generate_form_num = form_num + 1
            self.generate_form(request, generate_form_num)
            self.errors = None

    def generate_form(self, request, destination_form):
        self.form = add_new_good_forms(request, self.application_id)[destination_form]
        self.form_num = destination_form
        self.data["form_pk"] = destination_form
        self.add_hidden_fields()

    def add_hidden_fields(self):
        self.form.questions.append(HiddenField("form_pk", self.form_num))
        for fields_num in range(len(self.fields)):
            if fields_num != self.form_num:
                for field in self.fields[fields_num]:
                    if self.data.get(field, ""):
                        self.form.questions.append(HiddenField(field, self.data[field]))

    @staticmethod
    def add_prefix_to_errors(json, prefix):
        return {prefix + k: v for (k, v) in json.items()}


class DraftOpenGoodsTypeList(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        goods = get_application_goods_types(request, application_id)

        context = {
            "goods": goods,
            "application": application,
        }
        return render(request, "applications/goodstype/index.html", context)


class AddPreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        good, _ = get_good(request, str(kwargs["good_pk"]))
        title = strings.goods.AddPrexistingGoodToApplicationForm.TITLE
        context = {
            "title": title,
            "page": good_on_application_form(good, get_units(request), title),
        }
        return render(request, "form.html", context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        data, status_code = post_good_on_application(request, draft_id, request.POST)

        if status_code != HTTPStatus.CREATED:
            good, status_code = get_good(request, str(kwargs["good_pk"]))
            title = strings.goods.AddPrexistingGoodToApplicationForm.TITLE
            context = {
                "title": title,
                "page": good_on_application_form(good, get_units(request), title),
                "data": request.POST,
                "errors": data.get("errors"),
            }
            return render(request, "form.html", context)

        return redirect(reverse_lazy("applications:goods", kwargs={"pk": draft_id}))


class RemovePreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_on_application_id = str(kwargs["good_on_application_pk"])

        status_code = delete_application_preexisting_good(request, good_on_application_id)

        if status_code != 200:
            return error_page(request, "Unexpected error removing good")

        return redirect(reverse_lazy("applications:goods", kwargs={"pk": application_id}))
