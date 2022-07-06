def get_cle_suggestions_json(goods):
    cle_suggestions_json = []
    for good_on_application in goods:
        good = good_on_application["good"]
        cle_suggestions_json.append(
            {
                "id": good_on_application["id"],
                "name": good["name"],
                "controlListEntries": {
                    "exporter": good["control_list_entries"],
                },
            }
        )
    return cle_suggestions_json
