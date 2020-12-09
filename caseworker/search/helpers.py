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
