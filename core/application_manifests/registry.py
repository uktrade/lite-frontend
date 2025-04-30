from typing import Type, Callable
from .base import BaseManifest


class ManifestRegistry:

    def __init__(self):
        self.manifests = {}

    def register(self, manifest_type: str) -> Callable:
        def _register(cls):
            self.manifests[manifest_type] = cls()
            return cls

        return _register

    def get_manifest(self, app: str, case_type: str) -> Type[BaseManifest]:
        return self.get_manifest_by_type(f"{app}_{case_type}")

    def get_manifest_by_type(self, manifest_type: str) -> Type[BaseManifest]:
        return self.manifests[manifest_type]


application_manifest_registry = ManifestRegistry()
