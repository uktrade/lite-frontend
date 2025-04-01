import rules


def is_indeterminate_export_licence_type_allowed(wizard):
    return rules.test_rule("can_exporter_apply_for_indeterminate_export_licence_type", wizard.request)
