from django.views.generic import RedirectView


class Logout(RedirectView):
    """This logout view replicates how an openid logout endpoint would work.

    This purposefully doesn't need to provide any additional functionality
    beyond just redirecting back to the provided value.
    """

    def get_redirect_url(self):
        return self.request.GET["post_logout_redirect_uri"]
