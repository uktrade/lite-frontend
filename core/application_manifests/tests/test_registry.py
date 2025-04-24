import pytest

from core.application_manifests.registry import ManifestRegistry


def test_register(mocker):
    registry = ManifestRegistry()

    MockManifest = mocker.Mock()
    _register = registry.register("some_application_type")
    _register(MockManifest)

    assert registry.get_manifest_by_type("some_application_type") == MockManifest()


def test_register_with_decorator():
    registry = ManifestRegistry()

    @registry.register("some_application_case_type")
    class MockManifest:
        pass

    assert isinstance(registry.get_manifest_by_type("some_application_case_type"), MockManifest)
    assert isinstance(registry.get_manifest("some_application", "case_type"), MockManifest)


def test_register_missing_manifest_type():
    registry = ManifestRegistry()
    with pytest.raises(KeyError):
        registry.get_manifest_by_type("some_application_type")


def test_register_missing_application_and_case_type():
    registry = ManifestRegistry()
    with pytest.raises(KeyError):
        registry.get_manifest("some_application", "some_case_type")
