from .request_data import build_request_data
from .classes.applications import Applications
from .classes.cases import Cases
from .classes.document_templates import DocumentTemplates
from .classes.ecju_queries import EcjuQueries
from .classes.goods import Goods
from .classes.goods_queries import GoodsQueries
from .classes.organisations import Organisations
from .classes.parties import Parties
from .classes.picklists import Picklists
from .classes.queues import Queues
from .classes.users import Users


class Builder:
    def __init__(self, api_client_config, context):
        self.context = context

        base_url = api_client_config["api_url"].rstrip("/")
        request_data = build_request_data(
            exporter_user=api_client_config["exporter"], gov_user=api_client_config["gov"]
        )

        self._build_seed_classes(base_url, request_data)
        self._seed_essential_data()

    def _build_seed_classes(self, base_url, request_data):
        kwargs = dict(base_url=base_url, request_data=request_data, context=self.context)

        self.users = Users(**kwargs)
        self.organisations = Organisations(**kwargs)
        self.goods = Goods(**kwargs)
        self.goods_queries = GoodsQueries(**kwargs)
        self.parties = Parties(**kwargs)
        self.ecju_queries = EcjuQueries(**kwargs)
        self.picklists = Picklists(**kwargs)
        self.cases = Cases(**kwargs)
        self.queues = Queues(**kwargs)
        self.document_templates = DocumentTemplates(**kwargs)
        self.applications = Applications(parties=self.parties, goods=self.goods, **kwargs)

    def _seed_essential_data(self):
        if not self.users.headers_initialised:
            self._initialise_headers()
        self.goods.add_good()

    def _initialise_headers(self):
        self.users.auth_gov_user()
        self.organisations.setup_org()
        self.organisations.setup_org_for_switching_organisations()
        self.users.auth_exporter_user()
        self.users.headers_initialised = True
