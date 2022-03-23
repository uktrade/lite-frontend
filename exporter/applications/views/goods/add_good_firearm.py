from core.auth.views import LoginRequiredMixin

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.firearms import FirearmCategoryForm


class AddGoodFirearmSteps:
    FIREARM_CATEGORY = "FIREARM_CATEGORY"


class AddGoodFirearm(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (AddGoodFirearmSteps.FIREARM_CATEGORY, FirearmCategoryForm),
    ]
