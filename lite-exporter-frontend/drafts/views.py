from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.shortcuts import render

from drafts.services import get_draft_applications


@login_required
def index(request):
    data, status_code = get_draft_applications(request)

    if status_code is not 200:
        return HttpResponseServerError()

    context = {
        'title': 'Drafts',
        'data': data,
        'applicationDeleted': request.GET.get('application_deleted')
    }
    return render(request, 'drafts/index.html', context)
