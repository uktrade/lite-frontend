from django.shortcuts import redirect


class ExportLicenceLicenceTypeProcessor:
    def __init__(self, request):
        self.request = request

    def process(self):
        return redirect("applications:apply")
