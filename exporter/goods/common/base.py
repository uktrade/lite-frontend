from dateutil.parser import parse
from django.urls import reverse
from http import HTTPStatus

from django.http import Http404
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.summaries.summaries import get_summary_type_for_good

from exporter.core.services import get_organisation
from exporter.goods.services import get_good


def product_detail_breadcrumbs():
    return [
        {
            "title": "Account home",
            "url": reverse("core:home"),
        },
        {
            "title": "Product list",
            "url": reverse("goods:goods"),
        },
    ]


class BaseProductDetails(LoginRequiredMixin, TemplateView):
    template_name = "goods/product-details.html"
    summary_type = None

    def get_breadcrumbs(self):
        breadcrumbs = product_detail_breadcrumbs()

        if reverse("goods:archived_goods") in self.request.META.get("HTTP_REFERER", ""):
            breadcrumbs.append(
                {
                    "title": "Archived products",
                    "url": reverse("goods:archived_goods"),
                },
            )

        return breadcrumbs

    @expect_status(
        HTTPStatus.OK,
        "Error retrieving good",
        "Unable to load product details",
    )
    def get_good(self, request, good_id):
        return get_good(request, good_id, full_detail=True)

    def dispatch(self, request, *args, **kwargs):
        if not self.summary_type:
            raise ValueError(f"No summary type specified for {self.__class__.__name__}")

        organisation_id = str(self.request.session.get("organisation"))
        self.organisation = get_organisation(self.request, organisation_id)

        good_id = str(self.kwargs["pk"])
        self.good, _ = self.get_good(self.request, good_id)

        summary_type = get_summary_type_for_good(self.good)
        if summary_type != self.summary_type:
            raise Http404(f"Incorrect summary type {summary_type} should be {self.summary_type}")

        return super().dispatch(request, *args, **kwargs)

    def get_summary(self):
        raise NotImplementedError(f"Implement `get_summary` on {self.__class__.__name__}")

    def get_archive_history(self):
        archive_history = []
        for item in self.good["archive_history"]:
            date_obj = parse(item["actioned_on"])
            user = f"{item['user']['first_name']} {item['user']['last_name']}"
            if item["is_archived"]:
                archive_history.append(
                    f"Archived by {user} at {date_obj.strftime('%H:%M')} on {date_obj.strftime('%d %B %Y')}"
                )
            else:
                archive_history.append(
                    f"Restored by {user} at {date_obj.strftime('%H:%M')} on {date_obj.strftime('%d %B %Y')}"
                )

        return archive_history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["good"] = self.good
        context["summary"] = self.get_summary()
        context["archive_history"] = self.get_archive_history()
        context["breadcrumbs"] = self.get_breadcrumbs()

        return context
