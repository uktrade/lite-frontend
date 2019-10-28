from ...seed_data.seed_data_classes.seed_class import SeedClass


class SeedDocumentTemplate(SeedClass):
    def add_template(self):
        picklist_paragraph = self.seed_picklist.add_letter_paragraph_picklist()
