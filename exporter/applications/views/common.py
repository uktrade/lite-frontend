import rules

from http import HTTPStatus

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from requests.exceptions import HTTPError
from urllib.parse import urlencode

from core.wizard.conditionals import C
from core.wizard.views import BaseSessionWizardView

from exporter.applications.constants import (
    ApplicationStatus,
    ExportLicenceSteps,
)
from exporter.applications.forms.appeal import AppealForm
from exporter.applications.forms.application_actions import (
    withdraw_application_confirmation,
    surrender_application_confirmation,
)
from exporter.applications.forms.common import (
    EditApplicationForm,
    application_copy_form,
    exhibition_details_form,
    ApplicationMajorEditConfirmationForm,
    ApplicationsListSortForm,
    LicenceTypeForm,
    ApplicationNameForm,
    ToldByAnOfficialForm,
)
from exporter.applications.helpers.check_your_answers import convert_application_to_check_your_answers
from exporter.applications.helpers.summaries import draft_summary
from exporter.applications.helpers.task_list_sections import get_reference_number_description
from exporter.applications.helpers.task_lists import get_application_task_list
from exporter.applications.helpers.validators import (
    validate_withdraw_application,
    validate_delete_draft,
    validate_surrender_application_and_update_case_status,
)
from exporter.applications.payloads import ExportLicencePayloadBuilder
from exporter.applications.services import (
    get_activity,
    get_application_history,
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
    post_export_licence_application,
)
from exporter.applications.views.conditionals import is_indeterminate_export_licence_type_allowed
from exporter.organisation.members.services import get_user

from exporter.core.constants import HMRC, APPLICANT_EDITING
from exporter.core.services import get_organisation
from lite_content.lite_exporter_frontend import (
    applications,
    strings,
)
from lite_forms.generators import confirm_form
from lite_forms.views import SingleFormView, MultiFormView
from exporter.applications.forms.hcsat import HCSATminiform
from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.helpers import get_document_data


class ApplicationMixin(LoginRequiredMixin):

    @property
    def application_id(self):
        return str(self.kwargs["pk"])

    @property
    def application(self):
        return get_application(self.request, self.application_id)

    def get_application_detail_url(self):
        return reverse("applications:application", kwargs={"pk": self.application_id})

    def get_application_task_list_url(self, pk):
        return reverse("applications:task_list", kwargs={"pk": pk})


class ApplicationsList(LoginRequiredMixin, FormView):
    template_name = "applications/applications.html"
    form_class = ApplicationsListSortForm
    filters = [
        {
            "name": "Submitted",
            "filter": "submitted_applications",
        },
        {
            "name": "Finalised",
            "filter": "finalised_applications",
        },
        {
            "name": "Drafts",
            "filter": "draft_applications",
            "sort_by": "-created_at",
        },
        {
            "name": "Archived",
            "filter": "archived_applications",
        },
    ]

    def get_initial(self):
        return {
            "sort_by": self.request.GET.get("sort_by", "-submitted_at"),
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["action"] = reverse("applications:applications")
        return kwargs

    def get_tabs(self):
        tabs = []
        for tab in self.filters:
            sort_by = tab.get("sort_by", "-submitted_at")
            query_params = {"selected_filter": tab["filter"], "sort_by": sort_by}
            tab["url"] = f"/applications/?{urlencode(query_params, doseq=True)}"
            tabs.append(tab)

        return tabs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_filter = self.request.GET.get("selected_filter", "submitted_applications")
        params = {
            "page": int(self.request.GET.get("page", 1)),
            "selected_filter": selected_filter,
            "sort_by": self.request.GET.get("sort_by", "-submitted_at"),
        }

        organisation = get_organisation(self.request, self.request.session["organisation"])
        applications = get_applications(self.request, **params)
        is_user_multiple_organisations = len(get_user(self.request)["organisations"]) > 1

        return {
            **context,
            "applications": applications,
            "organisation": organisation,
            "tabs": self.get_tabs(),
            "selected_filter": selected_filter,
            "page": params.pop("page"),
            "is_user_multiple_organisations": is_user_multiple_organisations,
            "show_sort_options": selected_filter != "draft_applications",
        }


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


class ApplicationEditType(ApplicationMixin, FormView):
    """This is essentially now a temporary confirmation view before making a major edit"""

    form_class = EditApplicationForm
    template_name = "edit_application_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "application_id": self.application_id,
            "data": self.application,
        }

    def get_success_url(self):
        return self.get_application_task_list_url(self.application_id)

    @expect_status(
        HTTPStatus.OK,
        "Error updating status",
        "Unexpected error changing application status to APPLICANT_EDITING",
    )
    def handle_major_edit(self):
        return set_application_status(self.request, self.application_id, APPLICANT_EDITING)

    def form_valid(self, form):

        self.handle_major_edit()

        return super().form_valid(form)


class ApplicationMajorEditConfirmView(ApplicationMixin, FormView):
    """
    This is the confirmation page for whitelisted organisation before amending
    an application by copy
    """

    form_class = ApplicationMajorEditConfirmationForm
    template_name = "core/form.html"
    amended_application_id = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["application_reference"] = self.application["name"]
        kwargs["cancel_url"] = self.get_application_detail_url()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "back_link_url": self.get_application_detail_url(),
        }

    def get_success_url(self):
        return self.get_application_task_list_url(self.amended_application_id)

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating amendment",
        "Unexpected error creating amendment",
    )
    def create_amendment(self):
        return create_application_amendment(self.request, self.application_id)

    def handle_major_edit(self):

        data, _ = self.create_amendment()
        self.amended_application_id = data["id"]

    def form_valid(self, form):

        self.handle_major_edit()

        return super().form_valid(form)


class ApplicationTaskList(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application = get_application(request, kwargs["pk"])
        if application["status"]["key"] not in [ApplicationStatus.DRAFT, ApplicationStatus.APPLICANT_EDITING]:
            return redirect(reverse("applications:application", kwargs={"pk": kwargs["pk"]}))
        return get_application_task_list(request, application)

    def post(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, str(kwargs["pk"]))
        data, status_code = submit_application(request, application_id)

        if status_code != HTTPStatus.OK:
            return get_application_task_list(request, application, errors=data.get("errors"))

        return redirect("applications:summary", pk=application_id)


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
            "status_is_terminal": status_props["is_terminal"],
            "errors": kwargs.get("errors"),
            "text": kwargs.get("text", ""),
            "activity": get_activity(request, self.application_id) or {},
            "application_history": get_application_history(self.request, self.application_id),
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
                "answers": {**convert_application_to_check_your_answers(self.application, is_summary=True)},
                "summary_page": True,
                "application_type": applications.ApplicationPage.Summary.Licence.STANDARD,
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


class ExportLicenceView(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (ExportLicenceSteps.LICENCE_TYPE, LicenceTypeForm),
        (ExportLicenceSteps.APPLICATION_NAME, ApplicationNameForm),
        (ExportLicenceSteps.TOLD_BY_AN_OFFICIAL, ToldByAnOfficialForm),
    ]

    condition_dict = {
        ExportLicenceSteps.LICENCE_TYPE: ~C(is_indeterminate_export_licence_type_allowed),
    }

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse("apply_for_a_licence:start")
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_payload(self, form_dict):
        return ExportLicencePayloadBuilder().build(form_dict)

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating export licence application",
        "Unexpected error creating export licence application",
    )
    def post_export_licence_application(self, data):
        return post_export_licence_application(self.request, data)

    def get_success_url(self):
        return reverse("applications:task_list", kwargs={"pk": self.application["id"]})

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        self.application, _ = self.post_export_licence_application(data)
        return redirect(self.get_success_url())
