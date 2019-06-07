from django.urls import reverse_lazy


def create_persistent_bar(draft):
    return {
        'caption': 'Currently viewing:',
        'text': draft.get('name'),
        'url': reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft.get('id')}),
    }
