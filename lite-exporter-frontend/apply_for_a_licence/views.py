from django.urls import reverse_lazy

from applications.services import post_applications
from apply_for_a_licence.forms import initial_questions
from lite_forms.views import MultiFormView


class InitialQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = initial_questions()
        self.action = post_applications

    def get_success_url(self):
        pk = self.get_validated_data()['id']
        return reverse_lazy('applications:task_list', kwargs={'pk': pk})
