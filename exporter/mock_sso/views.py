from core.mock_sso.views import Logout as CoreLogout


class Logout(CoreLogout):
    def get_redirect_url(self):
        return self.request.GET["post_logout_redirect_uri"]
