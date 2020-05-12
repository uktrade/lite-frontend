from lite_forms.components import Custom


class PicklistPicker(Custom):
    def __init__(self, target, items):
        self.target = target
        super().__init__(template="components/picklist-picker.html", data=items)
