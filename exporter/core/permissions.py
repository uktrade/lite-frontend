from django.http import Http404

from core.services import get_organisation


def validate_is_in_organisation_type(request, organisation_types):
    """
    Raises an exception if the user's organisation is not inside of
    organisation_types
    organisation_types can be a string or list,
    expected values contain: 'hmrc', 'commercial', 'individual'
    """
    organisation = get_organisation(request, request.user.organisation)

    if not organisation["type"]["key"] in organisation_types:
        raise Http404
