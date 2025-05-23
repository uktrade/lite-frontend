from core.application_manifests.base import BaseManifest
from core.application_manifests.contants import ManifestType
from core.application_manifests.registry import application_manifest_registry
from .application_urls import StandardApplicationExporterUrls


@application_manifest_registry.register(ManifestType.EXPORTER_STANDARD_APPLICATION.value)
class StandardApplicationExporterManifest(BaseManifest):
    service_name = "apply for a standard individual export licence (SIEL)"
    urls = StandardApplicationExporterUrls
