from core.application_manifests.registry import application_manifest_registry


@application_manifest_registry.register("MADEUP_CASE_TYPE")
class MockManifest:
    pass
