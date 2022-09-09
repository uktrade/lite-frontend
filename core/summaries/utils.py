def pick_fields(summary, fields):
    filtered_summary = tuple((key, *rest) for key, *rest in summary if key in fields)
    sorted_summary = tuple(sorted(filtered_summary, key=lambda val: fields.index(val[0])))

    return sorted_summary


def remove_fields(summary, fields):
    filtered_summary = tuple((key, *rest) for key, *rest in summary if key not in fields)

    return filtered_summary


def get_field(summary, key):
    for field in summary:
        if field[0] == key:
            return field
    raise KeyError(f"{key} not found in summary")


def pluck_field(summary, key):
    found_field = get_field(summary, key)
    return found_field, remove_fields(summary, [key])
