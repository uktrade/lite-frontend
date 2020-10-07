import directory_client_core.base

from django.conf import settings


URL_APPLICATION = "/api/spire_dms/application/"
URL_LICENCE = "/api/spire_dms/licence/"


class SpireClient(directory_client_core.base.AbstractAPIClient):
    version = 1  # AbstractAPIClient exposes this in UserAgent header

    def list_licences(self, **params):
        return self.get(URL_LICENCE, params=params)

    def list_applications(self, **params):
        return self.get(URL_APPLICATION, params=params)

    def get_licence(self, pk):
        return self.get(f"{URL_LICENCE}{pk}/")

    def get_application(self, pk):
        return self.get(f"{URL_APPLICATION}{pk}/")


spire_client = SpireClient(
    base_url=settings.LITE_SPIRE_DMS_ARCHIVE_CLIENT_BASE_URL,
    api_key=settings.LITE_SPIRE_DMS_ARCHIVE_CLIENT_HAWK_SECRET,
    sender_id=settings.LITE_SPIRE_DMS_ARCHIVE_CLIENT_HAWK_SENDER_ID,
    timeout=settings.LITE_SPIRE_DMS_ARCHIVE_CLIENT_DEFAULT_TIMEOUT,
)
