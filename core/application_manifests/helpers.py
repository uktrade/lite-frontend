from core.application_manifests.registry import application_manifest_registry


def get_caseworker_manifest_for_case(case):
    return application_manifest_registry.get_manifest("CASEWORKER", case["case_type"]["type"]["key"])


def get_exporter_manifest_for_case(case):
    return application_manifest_registry.get_manifest("EXPORTER", case["case_type"]["type"]["key"])
