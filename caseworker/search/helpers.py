from copy import deepcopy


def group_results_by_combination(results):
    """
    This function groups results by a distinct combination of control list entry and report summary
    and regime, using frozenset objects as keys in the grouped results dictionary.
    """
    grouped_results = deepcopy(results)

    for item in grouped_results["results"]:
        item["distinct_combination_hits"] = []
        item["remaining_hits"] = []
        distinct_combinations = {}
        for hit in item["inner_hits"]["hits"]:
            combinations_key = frozenset(
                [
                    frozenset(cle["rating"] for cle in hit["control_list_entries"]),
                    hit["report_summary"],
                    frozenset(regime_entry["name"] for regime_entry in hit["regime_entries"]),
                ]
            )
            if combinations_key not in distinct_combinations:
                distinct_combinations[combinations_key] = hit["id"]
                item["distinct_combination_hits"].append(hit)
            else:
                item["remaining_hits"].append(hit)

        item.pop("inner_hits")

    return grouped_results
