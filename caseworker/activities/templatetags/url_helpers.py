from django import template

from core.application_manifests.helpers import get_caseworker_manifest_for_application_reference

register = template.Library()


@register.simple_tag
def get_notes_and_timelines_url(case_id, reference_code, queue_pk):
    manifest = get_caseworker_manifest_for_application_reference(reference_code)
    return manifest.urls.get_notes_and_timeline_url(case_id=case_id, queue_pk=queue_pk)
