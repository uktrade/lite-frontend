from lite_forms.components import Form, Filter, Checkboxes, TextArea, BackLink


def flags_form(flags, level, origin, url):
    return Form(
        title="Edit " + level + " flags",
        questions=[
            Filter(placeholder="Filter flags"),
            Checkboxes(title="Select all flags that apply", name="flags", options=flags),
            TextArea(
                name="note",
                title="Notes",
                description="Provide reasons for editing the flags on these " + level,
                optional=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=BackLink("Back to " + origin, url),
    )
