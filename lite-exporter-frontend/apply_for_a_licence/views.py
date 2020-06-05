from django.urls import reverse_lazy

from applications.services import post_applications, post_open_general_licences_applications
from apply_for_a_licence.forms.open_general_licences import open_general_licence_forms

from apply_for_a_licence.forms.triage_questions import (
    opening_question,
    export_licence_questions,
    MOD_questions,
    transhipment_questions,
    trade_control_licence_questions,
)
from apply_for_a_licence.validators import validate_opening_question, validate_open_general_licences
from conf.constants import PERMANENT, CaseTypes
from lite_forms.views import SingleFormView, MultiFormView


class LicenceType(SingleFormView):
    def init(self, request, **kwargs):
        self.form = opening_question()
        self.action = validate_opening_question

    def get_success_url(self):
        licence_type = self.get_validated_data()["licence_type"]
        return reverse_lazy(f"apply_for_a_licence:{licence_type}_questions")


class ExportLicenceQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = export_licence_questions(request, None)

    def get_action(self):
        if self.request.POST.get("application_type") == CaseTypes.OGEL:
            return post_open_general_licences_applications
        else:
            return post_applications

    def on_submission(self, request, **kwargs):
        copied_req = request.POST.copy()
        self.forms = export_licence_questions(
            request, copied_req.get("application_type"), copied_req.get("goodstype_category")
        )

    def get_success_url(self):
        if self.request.POST.get("application_type") == CaseTypes.OGEL:
            return reverse_lazy("apply_for_a_licence:ogl_questions", kwargs={"ogl": CaseTypes.OGEL})
        else:
            pk = self.get_validated_data()["id"]
            return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class TradeControlLicenceQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = trade_control_licence_questions(request)
        self.action = post_applications

    def get_success_url(self):
        if self.request.POST.get("application_type") == CaseTypes.OGTCL:
            return reverse_lazy("apply_for_a_licence:ogl_questions", kwargs={"ogl": CaseTypes.OGTCL})
        else:
            pk = self.get_validated_data()["id"]
            return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class TranshipmentQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = transhipment_questions(request)
        self.action = post_applications
        self.data = {"export_type": PERMANENT}

    def get_success_url(self):
        if self.request.POST.get("application_type") == CaseTypes.OGTL:
            return reverse_lazy("apply_for_a_licence:ogl_questions", kwargs={"ogl": CaseTypes.OGTL})
        else:
            pk = self.get_validated_data()["id"]
            return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class MODClearanceQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = MOD_questions(None)
        self.action = post_applications

    def on_submission(self, request, **kwargs):
        self.forms = MOD_questions(request.POST.copy().get("application_type"))

    def get_success_url(self):
        pk = self.get_validated_data()["id"]
        return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class OpenGeneralLicenceQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = open_general_licence_forms(request, **kwargs)
        self.action = validate_open_general_licences
