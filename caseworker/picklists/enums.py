from lite_content.lite_internal_frontend.picklists import PicklistCategory


class PicklistCategories:
    class Picklist:
        def __init__(self, name, key):
            self.name = name
            self.key = key

    proviso = Picklist(PicklistCategory.PROVISO, "proviso")
    ecju_query = Picklist(PicklistCategory.STANDARD_ECJU_QUERIES, "ecju_query")
    pre_visit_questionnaire = Picklist(PicklistCategory.PRE_VISIT_QUESTIONNAIRES, "pre_visit_questionnaire")
    compliance_actions = Picklist(PicklistCategory.COMPLIANCE_ACTIONS, "compliance_actions")
    letter_paragraph = Picklist(PicklistCategory.LETTER_PARAGRAPHS, "letter_paragraph")
    report_summary = Picklist(PicklistCategory.REPORT_SUMMARIES, "report_summary")
    standard_advice = Picklist(PicklistCategory.STANDARD_ADVICE, "standard_advice")
    footnotes = Picklist(PicklistCategory.FOOTNOTES, "footnotes")

    @classmethod
    def all(cls):
        return [
            cls.proviso,
            cls.ecju_query,
            cls.pre_visit_questionnaire,
            cls.compliance_actions,
            cls.letter_paragraph,
            cls.report_summary,
            cls.standard_advice,
            cls.footnotes,
        ]
