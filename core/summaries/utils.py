def pick_fields(summary, fields):
    filtered_summary = tuple((key, *rest) for key, *rest in summary if key in fields)
    sorted_summary = tuple(sorted(filtered_summary, key=lambda val: fields.index(val[0])))

    return sorted_summary
