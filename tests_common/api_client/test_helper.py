from .sub_helpers.documents import Documents
from .sub_helpers.applications import Applications
from .sub_helpers.cases import Cases
from .sub_helpers.document_templates import DocumentTemplates
from .sub_helpers.ecju_queries import EcjuQueries
from .sub_helpers.goods import Goods
from .sub_helpers.goods_queries import GoodsQueries
from .sub_helpers.organisations import Organisations
from .sub_helpers.parties import Parties
from .sub_helpers.picklists import Picklists
from .sub_helpers.queues import Queues
from .sub_helpers.users import Users


class TestHelper:
    """
    Contains a collection of test helper classes, grouped by functional area, with each class containing
    required logic wrapping calls to various LITE API endpoints.

    Generic request_data is automatically built.  If customisation of request_data is required,
    this is possible by constructing individual sub-helpers directly and passing the custom request data to them.
    """

    def __init__(self, api):
        self.api_client = api
        self.context = self.api_client.context

        request_data = self.api_client.request_data

        self.documents = Documents(api_client=self.api_client, request_data=request_data)
        self.users = Users(api_client=self.api_client, request_data=request_data)
        self.organisations = Organisations(api_client=self.api_client, request_data=request_data)
        self.goods = Goods(api_client=self.api_client, documents=self.documents, request_data=request_data)
        self.goods_queries = GoodsQueries(api_client=self.api_client, request_data=request_data)
        self.parties = Parties(api_client=self.api_client, documents=self.documents, request_data=request_data)
        self.ecju_queries = EcjuQueries(api_client=self.api_client, request_data=request_data)
        self.picklists = Picklists(api_client=self.api_client, request_data=request_data)
        self.cases = Cases(api_client=self.api_client, request_data=request_data)
        self.queues = Queues(api_client=self.api_client, request_data=request_data)
        self.document_templates = DocumentTemplates(api_client=self.api_client, request_data=request_data)
        self.applications = Applications(
            parties=self.parties,
            goods=self.goods,
            api_client=self.api_client,
            documents=self.documents,
            request_data=request_data,
        )


def build_test_helper(config):
    test_helper = TestHelper(config)
    _seed_essential_data(test_helper)
    return test_helper


def _seed_essential_data(test_helper):
    if not test_helper.api_client.headers_initialised:
        _initialise_headers(test_helper)
    test_helper.goods.add_good()


def _initialise_headers(test_helper):
    test_helper.api_client.auth_gov_user()
    test_helper.organisations.setup_org()
    test_helper.organisations.setup_org_for_switching_organisations()
    test_helper.api_client.auth_exporter_user()
    test_helper.api_client.headers_initialised = True
