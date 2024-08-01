from functools import cached_property

import rules
from django.shortcuts import redirect
from core.auth.views import LoginRequiredMixin
from exporter.ecju_queries.ecju_forms import ECJUQueryRespondForm, ECJUQueryRespondConfirmForm

from django.views.generic import FormView
from django.urls import reverse_lazy, reverse

from exporter.applications.services import get_application
from exporter.ecju_queries.services import get_ecju_query, get_ecju_query_documents, put_ecju_query


class ECJURespondMixin:
    @cached_property
    def case_id(self):
        return str(self.kwargs["case_pk"])

    @cached_property
    def application(self):
        return get_application(self.request, self.case_id)

    @cached_property
    def ecju_query_id(self):
        return str(self.kwargs["query_pk"])

    @cached_property
    def ecju_query(self):
        return get_ecju_query(self.request, self.case_id, self.ecju_query_id)

    @cached_property
    def ecju_query_documents(self):
        return get_ecju_query_documents(self.request, self.case_id, self.ecju_query_id)

    @cached_property
    def ecju_response_key(self):
        return f"{self.ecju_query_id}_response"

    @property
    def session_ecju_response(self):
        if self.ecju_response_key in self.request.session.keys():
            return self.request.session[self.ecju_response_key]

    @session_ecju_response.setter
    def session_ecju_response(self, value):
        if value:
            self.request.session[self.ecju_response_key] = value

    def delete_ecju_response_from_session(self):
        if self.ecju_response_key in self.request.session.keys():
            del self.request.session[self.ecju_response_key]

    def get_back_url(self):
        return reverse_lazy("applications:application", kwargs={"pk": self.case_id, "type": "ecju-queries"})


class ECJURespondQueryView(LoginRequiredMixin, ECJURespondMixin, FormView):
    template_name = "core/form.html"
    form_class = ECJUQueryRespondForm

    # This is required because of some legacy code that depends on object_type when adding a document
    OBJECT_TYPE = "application"

    def get_edit_url(self):
        if not rules.test_rule("can_invoke_major_editable", self.request, self.application):
            return None

        if rules.test_rule("can_amend_by_copy", self.request, self.application):
            return reverse("applications:major_edit_confirm", kwargs={"pk": self.case_id})

        return reverse("applications:edit_type", kwargs={"pk": self.case_id})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["ecju_query"] = self.ecju_query
        form_kwargs["documents"] = self.ecju_query_documents
        form_kwargs["case_id"] = self.case_id
        form_kwargs["ecju_response"] = self.session_ecju_response
        form_kwargs["edit_url"] = self.get_edit_url()
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy(
            "ecju_queries:respond_to_application_query_confirm",
            kwargs={"query_pk": self.ecju_query_id, "case_pk": self.case_id},
        )

    def form_valid(self, form):
        data = form.cleaned_data
        post_keys = self.request.POST.keys()
        self.session_ecju_response = data["response"]
        if "add_document" in post_keys:
            return redirect(
                reverse(
                    "ecju_queries:add_supporting_document",
                    kwargs={
                        "query_pk": self.ecju_query_id,
                        "object_type": self.OBJECT_TYPE,
                        "case_pk": self.case_id,
                        "extra_pk": self.case_id,
                    },
                )
            )
        elif "delete_document" in post_keys:
            return redirect(
                reverse(
                    "ecju_queries:query-document-delete",
                    kwargs={
                        "query_pk": self.ecju_query_id,
                        "object_type": self.OBJECT_TYPE,
                        "case_pk": self.case_id,
                        "extra_pk": self.case_id,
                        "doc_pk": self.request.POST["delete_document"],
                    },
                )
            )
        elif "cancel" in post_keys:
            self.delete_ecju_response_from_session()
            return redirect(self.get_back_url())

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_back_url()
        context["back_link_text"] = "back to ecju queries"
        context["form_title"] = self.form_class.Layout.TITLE
        return context


class ECJURespondQueryConfirmView(LoginRequiredMixin, ECJURespondMixin, FormView):
    template_name = "core/form.html"
    form_class = ECJUQueryRespondConfirmForm

    def get_success_url(self):
        return reverse_lazy("applications:application", kwargs={"pk": self.case_id, "type": "ecju-queries"})

    def form_valid(self, form):
        post_data = {"response": self.session_ecju_response} if self.session_ecju_response else {}
        self.delete_ecju_response_from_session()

        if "cancel" in self.request.POST.keys():
            return redirect(self.get_back_url())
        put_ecju_query(self.request, self.case_id, self.ecju_query_id, post_data)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse(
            "ecju_queries:respond_to_application_query",
            kwargs={"query_pk": self.ecju_query_id, "case_pk": self.case_id},
        )
        context["back_link_text"] = "back to edit response"
        context["form_title"] = self.form_class.Layout.TITLE
        return context
