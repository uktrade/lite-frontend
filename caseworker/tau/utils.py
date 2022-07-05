def get_cle_suggestions_json(goods):
    cle_suggestions_json = []
    for good_on_application in goods:
        good = good_on_application["good"]

        # The CLE entries in the good object could either be the exporters CLE entries or it could possibly be
        # from previous assessments.
        # What we do know is that if there are no precedents then the CLE entry in the good object MUST be the one
        # from the exporter (I'm sure there are edge cases where that might not be true but this is the best we
        # have to go on).
        # Once an assessment has been made we no longer know, nor care about the exporters original CLE entries so
        # we don't need to try to set this in any way.
        exporter_cle_entry = [cle["rating"] for cle in good["control_list_entries"]]
        precedents = []
        precedent = good_on_application.get("precedent")
        if precedent:
            exporter_cle_entry = []
            precedents = [precedent["control_list_entries"]]

        cle_suggestions_json.append(
            {
                "id": good_on_application["id"],
                "name": good["name"],
                "controlListEntries": {
                    "exporter": exporter_cle_entry,
                    "precedents": precedents,
                },
            }
        )
    return cle_suggestions_json
