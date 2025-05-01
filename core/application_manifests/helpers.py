from typing import Type
from core.application_manifests.base import BaseManifest

from core.application_manifests.contants import ManifestType
from core.application_manifests.registry import application_manifest_registry


def get_caseworker_manifest_for_application_reference(reference_code: str) -> Type[BaseManifest]:
    if reference_code and reference_code.startswith("F680"):
        return application_manifest_registry.get_manifest_by_type(ManifestType.CASEWORKER_F680.value)
    return application_manifest_registry.get_manifest_by_type(ManifestType.CASEWORKER_STANDARD_APPLICATION.value)


def get_exporter_manifest_for_application_reference(reference_code: str) -> Type[BaseManifest]:
    if reference_code and reference_code.startswith("F680"):
        return application_manifest_registry.get_manifest_by_type(ManifestType.EXPORTER_F680.value)
    return application_manifest_registry.get_manifest_by_type(ManifestType.EXPORTER_STANDARD_APPLICATION.value)
