from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import View


class NotesAndTimelineAll(View):
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAG_NOTES_TIMELINE_2_0:
            raise Http404("Feature flag disabled")
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")
