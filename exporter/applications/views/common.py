import rules

from http import HTTPStatus

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from requests.exceptions import HTTPError

from exporter.applications.forms.appeal import AppealForm
from exporter.applications.forms.application_actions import (
    withdraw_application_confirmation,
    surrender_application_confirmation,
)
from exporter.applications.forms.common import (
    EditApplicationForm,
    application_copy_form,
    exhibition_details_form,
)
from exporter.applications.helpers.check_your_answers import (
    convert_application_to_check_your_answers,
    get_application_type_string,
)
from exporter.applications.helpers.summaries import draft_summary
from exporter.applications.helpers.task_list_sections import get_reference_number_description
from exporter.applications.helpers.task_lists import get_application_task_list
from exporter.applications.helpers.validators import (
    validate_withdraw_application,
    validate_delete_draft,
    validate_surrender_application_and_update_case_status,
)
from exporter.applications.services import (
    get_activity,
    get_applications,
    get_case_notes,
    get_case_generated_documents,
    get_application_ecju_queries,
    post_case_notes,
    post_survey_feedback,
    submit_application,
    get_application,
    set_application_status,
    get_status_properties,
    copy_application,
    post_exhibition,
    post_appeal,
    post_appeal_document,
    get_appeal,
    create_application_amendment,
)
from exporter.organisation.members.services import get_user

from exporter.core.constants import HMRC, APPLICANT_EDITING, NotificationType
from exporter.core.helpers import str_to_bool
from exporter.core.services import get_organisation
from lite_content.lite_exporter_frontend import strings
from lite_forms.generators import confirm_form
from lite_forms.views import SingleFormView, MultiFormView
from exporter.applications.forms.hcsat import HCSATminiform
from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.helpers import convert_dict_to_query_params, get_document_data


class ApplicationsList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        params = {
            "page": int(request.GET.get("page", 1)),
            "submitted": str_to_bool(request.GET.get("submitted", True)),
            "finalised": str_to_bool(request.GET.get("finalised", False)),
            "sort": request.GET.get("sort", "submitted_at"),
        }
        organisation = get_organisation(request, request.session["organisation"])
        applications = get_applications(request, **params)
        is_user_multiple_organisations = len(get_user(self.request)["organisations"]) > 1
        context = {
            "applications": applications,
            "organisation": organisation,
            "params": params,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
            "is_user_multiple_organisations": is_user_multiple_organisations,
        }
        return render(
            request, "applications/applications.html" if params["submitted"] else "applications/drafts.html", context
        )


class DeleteApplication(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = confirm_form(
            title=strings.applications.DeleteApplicationPage.TITLE,
            confirmation_name="choice",
            summary=draft_summary(application),
            back_link_text=strings.applications.DeleteApplicationPage.BACK_TEXT,
            yes_label=strings.applications.DeleteApplicationPage.YES_LABEL,
            no_label=strings.applications.DeleteApplicationPage.NO_LABEL,
            submit_button_text=strings.applications.DeleteApplicationPage.SUBMIT_BUTTON,
            back_url=request.GET.get("return_to"),
            side_by_side=True,
        )
        self.action = validate_delete_draft

    def get_success_url(self):
        if self.get_validated_data().get("status"):
            return reverse_lazy("applications:applications") + "?submitted=False"
        else:
            return self.request.GET.get("return_to")


class ApplicationEditType(LoginRequiredMixin, FormView):
    form_class = EditApplicationForm
    template_name = "edit_application_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.application_id = str(self.kwargs["pk"])
        self.data = get_application(self.request, self.application_id)

        context.update(
            {
                "application_id": self.application_id,
                "data": self.data,
            }
        )
        return context

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating amendment",
        "Unexpected error creating amendment",
    )
    def create_amendment(self):
        return create_application_amendment(self.request, str(self.kwargs["pk"]))

    def handle_major_edit(self):
        organisation = get_organisation(self.request, self.request.session["organisation"])
        if organisation["id"] in settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS:
            data, _ = self.create_amendment()
            return redirect(reverse_lazy("applications:task_list", kwargs={"pk": data["id"]}))
        else:
            set_application_status(self.request, self.application_id, APPLICANT_EDITING)
            return redirect(reverse_lazy("applications:task_list", kwargs={"pk": self.application_id}))

    def form_valid(self, form):

        self.application_id = str(self.kwargs["pk"])
        if form.cleaned_data.get("edit_type") == "major":
            return self.handle_major_edit()

        return HttpResponseRedirect(reverse_lazy("applications:task_list", kwargs={"pk": self.application_id}))


class ApplicationTaskList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application = get_application(request, kwargs["pk"])
        return get_application_task_list(request, application)

    def post(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, str(kwargs["pk"]))
        data, status_code = submit_application(request, application_id)

        if status_code != HTTPStatus.OK:
            return get_application_task_list(request, application, errors=data.get("errors"))

        if application.sub_type not in [NotificationType.EUA, NotificationType.GOODS]:
            # All other application types direct to the summary page
            return HttpResponseRedirect(reverse_lazy("applications:summary", kwargs={"pk": application_id}))
        else:
            # Redirect to the success page to prevent the user going back after the Post
            # Follows this pattern: https://en.wikipedia.org/wiki/Post/Redirect/Get
            return HttpResponseRedirect(reverse_lazy("applications:success_page", kwargs={"pk": application_id}))


class ApplicationDetail(LoginRequiredMixin, TemplateView):
    application_id = None
    application = None
    case_id = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs["pk"])
        self.application = get_application(request, self.application_id)
        self.case_id = self.application["case"]
        self.view_type = kwargs.get("type")

        return super(ApplicationDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        status_props, _ = get_status_properties(request, self.application["status"]["key"])

        context = {
            "case_id": self.application_id,
            "application": self.application,
            "type": self.view_type,
            "answers": convert_application_to_check_your_answers(self.application),
            "status_is_read_only": status_props["is_read_only"],
            "status_is_terminal": status_props["is_terminal"],
            "errors": kwargs.get("errors"),
            "text": kwargs.get("text", ""),
            "activity": get_activity(request, self.application_id) or {},
        }

        if self.application.sub_type != HMRC:
            if self.view_type == "case-notes":
                context["notes"] = get_case_notes(request, self.case_id)["case_notes"]

            if self.view_type == "ecju-queries":
                context["open_queries"], context["closed_queries"] = get_application_ecju_queries(request, self.case_id)

        if self.view_type == "generated-documents":
            generated_documents, _ = get_case_generated_documents(request, self.application_id)
            context["generated_documents"] = generated_documents["results"]

        return render(request, "applications/application.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        response, _ = post_case_notes(request, self.case_id, request.POST)

        if "errors" in response:
            return self.get(request, error=response["errors"], text=request.POST.get("text"), **kwargs)

        return redirect(
            reverse_lazy("applications:application", kwargs={"pk": self.application_id, "type": "case-notes"})
        )


class ApplicationSummary(LoginRequiredMixin, TemplateView):
    template_name = "applications/application.html"

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs["pk"])
        self.application = get_application(request, self.application_id)
        self.case_id = self.application["case"]
        return super(ApplicationSummary, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "case_id": self.application_id,
                "application": self.application,
                "answers": {**convert_application_to_check_your_answers(self.application, summary=True)},
                "summary_page": True,
                "application_type": get_application_type_string(self.application),
                "notes": get_case_notes(self.request, self.case_id)["case_notes"],
                "reference_code": get_reference_number_description(self.application),
            }
        )
        return context

    def post(self, request, **kwargs):
        return HttpResponseRedirect(reverse_lazy("applications:declaration", kwargs={"pk": self.application_id}))


class WithdrawApplication(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = withdraw_application_confirmation(application, self.object_pk)
        self.action = validate_withdraw_application
        self.success_url = reverse_lazy("applications:application", kwargs={"pk": self.object_pk})


class SurrenderApplication(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = surrender_application_confirmation(application, self.object_pk)
        self.action = validate_surrender_application_and_update_case_status
        self.success_url = reverse_lazy("applications:application", kwargs={"pk": self.object_pk})


class Notes(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        notes = get_case_notes(request, application_id)["case_notes"]

        context = {
            "application": application,
            "notes": notes,
            "post_url": reverse_lazy("applications:notes", kwargs={"pk": application_id}),
            "error": kwargs.get("error"),
            "text": kwargs.get("text", ""),
        }
        return render(request, "applications/case-notes.html", context)

    def post(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        response, _ = post_case_notes(request, application_id, request.POST)

        if "errors" in response:
            return self.get(request, error=response["errors"]["text"][0], text=request.POST.get("text"), **kwargs)

        return redirect(reverse_lazy("applications:notes", kwargs={"pk": application_id}))


class CheckYourAnswers(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = kwargs["pk"]
        application = get_application(request, application_id)

        context = {"application": application, "answers": {**convert_application_to_check_your_answers(application)}}
        return render(request, "applications/check-your-answers.html", context)


class Submit(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = kwargs["pk"]
        application = get_application(request, application_id)

        context = {
            "application": application,
        }
        return render(request, "applications/submit.html", context)


class ApplicationSubmitSuccessPage(LoginRequiredMixin, FormView):

    template_name = "applications/application-submit-success.html"
    form_class = HCSATminiform

    def get_application_url(self):
        return reverse(
            "applications:application",
            kwargs={"pk": self.kwargs["pk"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form_title"] = "Application submitted"
        context["back_link_url"] = self.get_application_url()
        application_id = self.kwargs["pk"]
        application = get_application(self.request, application_id)

        if application.status in ["draft", "applicant_editing"]:
            raise Http404
        context["reference_code"] = application["reference_code"]

        context["links"] = {
            "View your list of applications": reverse_lazy("applications:applications"),
            "Apply for another licence or clearance": reverse_lazy("apply_for_a_licence:start"),
            "Return to your export control account dashboard": reverse_lazy("core:home"),
        }

        return context

    @expect_status(
        HTTPStatus.CREATED,
        "Error sending feedback",
        "Unexpected error sending feedback",
    )
    def post_survey_feedback(self, request, data):
        return post_survey_feedback(request, data)

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        data["user_journey"] = "APPLICATION_SUBMISSION"
        survey, _ = self.post_survey_feedback(self.request, data)
        self.survey_id = survey["id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "applications:application-hcsat",
            kwargs={
                "pk": self.kwargs["pk"],
                "sid": self.survey_id,
            },
        )


class ApplicationCopy(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = application_copy_form(application.sub_type)
        self.action = copy_application

    def get_success_url(self):
        id = self.get_validated_data()["data"]
        return reverse_lazy("applications:task_list", kwargs={"pk": id})


class ExhibitionDetail(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = exhibition_details_form(self.object_pk)
        self.action = post_exhibition

    def get_data(self):
        data = self.data
        date_fields = ["first_exhibition_date", "required_by_date"]
        for field in date_fields:
            if data.get(field, False):
                date_split = data[field].split("-")
                data[field + "year"], data[field + "month"], data[field + "day"] = date_split
        return data

    def get_success_url(self):
        return reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})


class AppealApplication(LoginRequiredMixin, FormView):
    form_class = AppealForm
    template_name = "core/form.html"

    def dispatch(self, request, **kwargs):
        try:
            self.application = get_application(request, kwargs["case_pk"])
        except HTTPError:
            raise Http404()

        if not rules.test_rule("can_user_appeal_case", request, self.application):
            raise Http404()

        return super().dispatch(request, **kwargs)

    def get_application_url(self):
        return reverse(
            "applications:application",
            kwargs={"pk": self.kwargs["case_pk"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form_title"] = self.form_class.Layout.TITLE
        context["back_link_url"] = self.get_application_url()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["cancel_url"] = self.get_application_url()

        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:appeal_confirmation",
            kwargs={
                "case_pk": self.kwargs["case_pk"],
                "appeal_pk": self.appeal["id"],
            },
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating appeal",
        "Unexpected error creating appeal",
    )
    def post_appeal(self, request, application_pk, data):
        return post_appeal(request, application_pk, data)

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating appeal document",
        "Unexpected error creating appeal document",
    )
    def post_appeal_document(self, request, appeal_pk, data):
        return post_appeal_document(request, appeal_pk, data)

    def form_valid(self, form):
        cleaned_data = form.cleaned_data.copy()
        documents = cleaned_data.pop("documents")

        appeal, _ = self.post_appeal(
            self.request,
            self.application["id"],
            cleaned_data,
        )
        for document in documents:
            self.post_appeal_document(
                self.request,
                appeal["id"],
                get_document_data(document),
            )

        self.appeal = appeal

        return super().form_valid(form)


class AppealApplicationConfirmation(LoginRequiredMixin, TemplateView):
    template_name = "applications/appeal-confirmation.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            self.application = get_application(self.request, self.kwargs["case_pk"])
        except HTTPError:
            raise Http404()

        try:
            self.appeal = get_appeal(self.request, self.application["id"], self.kwargs["appeal_pk"])
        except HTTPError:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["application"] = get_application(self.request, self.kwargs["case_pk"])

        return context
