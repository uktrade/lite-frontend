class SeedClass:
    def __init__(self, base_url, gov_headers, export_headers, request_data, context):
        self.base_url = base_url
        self.gov_headers = gov_headers
        self.export_headers = export_headers
        self.request_data = request_data
        self.context = context

    def add_to_context(self, name, value):
        self.context[name] = value
