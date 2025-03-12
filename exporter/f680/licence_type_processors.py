from django.shortcuts import redirect

from http import HTTPStatus

from core.decorators import expect_status

from exporter.f680.services import post_f680_application


class F680LicenceLicenceTypeProcessor:
    def __init__(self, request):
        self.request = request

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 application",
        "Unexpected error creating F680 application",
    )
    def post_f680_application(self, data):
        return post_f680_application(self.request, data)

    def process(self):
        data = {"application": {}}
        response_data, _ = self.post_f680_application(data)
        return redirect("f680:summary", pk=response_data["id"])
