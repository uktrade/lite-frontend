from lite_forms.components import Option


def get_potential_ogl_control_list_entries(open_general_licences):
    control_list_entries = []

    for open_general_licence in open_general_licences:
        for control_list_entry in open_general_licence["control_list_entries"]:
            if control_list_entry not in control_list_entries:
                control_list_entries.append(control_list_entry)

    return_value = []
    for control_list_entry in control_list_entries:
        return_value.append(Option(control_list_entry["rating"], control_list_entry["rating"]))

    return return_value


def get_potential_ogl_countries(open_general_licences):
    countries = []

    for open_general_licence in open_general_licences:
        for country in open_general_licence["countries"]:
            if country not in countries:
                countries.append(country)

    return_value = []
    for country in countries:
        return_value.append(Option(country["id"], country["name"]))

    return return_value


def get_potential_ogl_sites(open_general_licences):
    sites = []

    for open_general_licence in open_general_licences:
        for registration in open_general_licence["registrations"]:
            if registration["site"] not in sites:
                sites.append(registration["site"])

    return_value = []
    for site in sites:
        return_value.append(Option(site["id"], site["name"]))

    return return_value
