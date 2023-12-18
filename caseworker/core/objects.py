class Tab:
    def __init__(self, id, name, url, count=0, has_template=True):
        self.id = "tab-" + id
        self.name = name
        self.url = url
        self.count = count
        self.has_template = has_template
