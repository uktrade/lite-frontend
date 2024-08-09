def get_latest_licence_status(case):
    licenses = case.get("licences")
    if licenses:
        sorted_licenses = sorted(licenses, key=lambda x: x["created_at"])
        return sorted_licenses[-1].get("status")
