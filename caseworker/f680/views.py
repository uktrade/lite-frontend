from django.views.generic import TemplateView

from caseworker.cases.services import get_case
from caseworker.queues.services import get_queue


class Section:
    def __init__(self, title):
        self.title = title


class ItemSection(Section):
    multi = False

    def __init__(self, title, item):
        super().__init__(title)
        self._item = item

    def details(self):
        return [{"name": field_name, "label": d["label"], "value": d["value"]} for field_name, d in self._item.items()]


class MultiItemSection(Section):
    multi = True

    def __init__(self, title, items):
        super().__init__(title)
        self._items = items

    def items(self):
        return [ItemSection(f"{self.title} {i}", item) for i, item in enumerate(self._items)]


class ApplicationDetails:
    def __init__(self, details, ordering):
        self.details = details
        self.ordering = ordering

    def sections(self):
        sections = []
        for key in sorted(self.details):
            section = self.details[key]
            if isinstance(section, dict):
                sections.append(ItemSection(key, section))
            elif isinstance(section, list):
                sections.append(MultiItemSection(key, section))

        return sections


class CaseDetailView(TemplateView):
    template_name = "f680/case/detail.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["case"] = self.case
        context_data["application_details"] = ApplicationDetails(
            self.case.data["application"],
            ["application", "products"],
        )

        return context_data
