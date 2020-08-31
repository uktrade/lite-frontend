from lite_forms.components import (
    FiltersBar,
    TextInput,
)


def case_search_box(request):
    return FiltersBar([TextInput(name="search_keyword", title="Search keyword"),],)
