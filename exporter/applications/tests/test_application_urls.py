from exporter.applications.application_urls import StandardApplicationExporterUrls


def test_check_all_get_url_methods_are_implemented():
    url_class = StandardApplicationExporterUrls

    method_list = [
        func if func.startswith("get") else None for func in dir(url_class) if callable(getattr(url_class, func))
    ]
    get_methods = list(filter(None, method_list))
    for method_name in get_methods:
        func = getattr(url_class, method_name)
        # Will raise a Not implemented error if method defined in base class is missing
        func(
            case_id="3913ff20-5a2b-468a-bf5d-427228459b06",
            queue_pk="3913ff20-5a2b-468a-bf5d-427228459b06",
            pk="3913ff20-5a2b-468a-bf5d-427228459b06",
        )
