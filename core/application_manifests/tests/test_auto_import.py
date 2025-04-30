from django.apps.registry import apps

from core.application_manifests.registry import ManifestRegistry


def test_registering_manifests(mocker):
    mock_application_manifest_registry = mocker.patch(
        "core.application_manifests.registry.application_manifest_registry",
        new_callable=ManifestRegistry,
    )
    apps.set_installed_apps(
        [
            "core.application_manifests",
            "core.application_manifests.tests.app_with_manifest",
        ]
    )
    manifest = mock_application_manifest_registry.get_manifest_by_type("MADEUP_CASE_TYPE")
    from core.application_manifests.tests.app_with_manifest.application_manifest import MockManifest

    assert isinstance(manifest, MockManifest)
    apps.unset_installed_apps()
