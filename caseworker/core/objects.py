class Tab:
    def __init__(self, id, name, url, count=0, has_template=True):
        self.id = "tab-" + id
        self.name = name
        self.url = url
        self.count = count
        self.has_template = has_template


class TabCollection:
    def __init__(self, id, name, children, count=0):
        self.id = "tab-collection-" + id
        self.name = name
        self.children = children if children else []
        self.count = count
