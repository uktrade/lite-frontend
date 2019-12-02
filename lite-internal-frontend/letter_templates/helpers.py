from letter_templates.services import get_letter_layout


def get_template_content(request):
    data = request.POST.copy()

    layout = None
    if data.get("layout"):
        layout, status = get_letter_layout(request, data["layout"])
        if status != 200:
            raise RuntimeError(f"Letter layout endpoint returned { status }.")

    return {
        "name": data.get("name"),
        "layout": layout,
        "case_types": data.getlist("case_types"),
        "action": data.get("action"),
        "letter_paragraphs": data.getlist("letter_paragraphs"),
    }
