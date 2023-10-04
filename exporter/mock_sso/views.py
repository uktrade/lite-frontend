from django.views.generic import RedirectView


class Logout(RedirectView):
    def get_redirect_url(self):
        return self.request.GET["post_logout_redirect_uri"]
