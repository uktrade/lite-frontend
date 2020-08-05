from lite_forms.components import Custom


class PicklistPicker(Custom):
    def __init__(self, target, type, set_text=True, title=None, description=None):
        self.target = target
        self.type = type
        self.set_text = set_text
        self.title = title
        self.description = description
        if not self.set_text:
            self.name = target
        super().__init__(template="components/picklist-picker.html")
