from copy import deepcopy

from django.utils.html import strip_tags, mark_safe


def highlight_results(results):
    for result in results:
        for dotted_path, highlights in result["highlight"].items():
            if dotted_path.endswith(".raw"):
                dotted_path = dotted_path[:-4]
            if highlights and dotted_path != "wildcard":
                *path, target = dotted_path.split(".")
                for item in keypath_lookup(result, path):
                    for highlight in highlights:
                        if item[target] == strip_tags(highlight):
                            item[target] = mark_safe(highlight)
                if not path and target in result:
                    for highlight in highlights:
                        result[target] = mark_safe(highlight)

        if "inner_hits" in result and "hits" in result["inner_hits"]:
            highlight_results(result["inner_hits"]["hits"])


def keypath_lookup(level, keys):
    for i, key in enumerate(keys):
        if isinstance(level[key], list):
            for level in level[key]:
                yield from keypath_lookup(level, keys[i + 1 :])
            else:
                break
        else:
            yield from keypath_lookup(level[key], keys[i + 1 :])
            break
    else:
        yield level


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
