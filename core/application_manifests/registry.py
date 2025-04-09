class ManifestRegistry:

    def __init__(self):
        self.manifests = {}

    def register(self, app, case_type):
        def _register(cls):
            self.manifests[f"{app}_{case_type}"] = cls()
            return cls

        return _register

    def get_manifest(self, app, case_type):
        return self.manifests[f"{app}_{case_type}"]


application_manifest_registry = ManifestRegistry()
