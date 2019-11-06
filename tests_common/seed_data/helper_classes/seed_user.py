from . import seed_class
from .. import make_requests


class SeedUser(seed_class.SeedClass):
    def add_user(self, data, url, token_name):
        token = make_requests.make_request('POST', base_url=self.base_url, url=url, body=data, headers=self.gov_headers).json()[
            'token']
        self.add_to_context(token_name, token)

    def auth_gov_user(self):
        self.add_user(self.request_data['gov_user'], '/gov-users/authenticate/', 'gov_user_token')
        self.gov_headers['gov-user-token'] = self.context['gov_user_token']

    def auth_export_user(self):
        self.add_user(self.request_data['export_user'], '/users/authenticate/', 'export_user_token')
        self.export_headers['exporter-user-token'] = self.context['export_user_token']
        self.export_headers['organisation-id'] = self.context['org_id']
