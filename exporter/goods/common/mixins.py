import requests

from django.http import Http404
from django.utils.functional import cached_property

from exporter.core.services import get_organisation
from exporter.goods.services import get_good


class ProductDetailsMixin:
    @cached_property
    def good_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def good(self):
        return get_good(self.request, self.good_id, full_detail=True)[0]

    def dispatch(self, request, *args, **kwargs):
        try:
            organisation_id = str(self.request.session.get("organisation"))
            self.organisation = get_organisation(self.request, organisation_id)
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)
