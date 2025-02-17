import rules


@rules.predicate
def is_exporter_in_organisation_list(request, organisation_list):
    return request.session["organisation"] in organisation_list


rules.add_rule(
    "exporter_in_organisation_list",
    is_exporter_in_organisation_list,
)
