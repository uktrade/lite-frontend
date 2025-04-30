from core.application_manifests.base import BaseManifest
from core.application_manifests.contants import ManifestType
from core.application_manifests.registry import application_manifest_registry
from .application_urls import F680CaseworkerUrls


@application_manifest_registry.register(ManifestType.CASEWORKER_F680.value)
class F680CaseworkerManifest(BaseManifest):
    urls = F680CaseworkerUrls
