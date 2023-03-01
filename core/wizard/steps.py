class Step:
    @property
    def form_class(self):
        raise NotImplementedError(f"`form_class` is a required attribute on {self.__class__.__name__}")

    def get_initial(self, view):
        raise NotImplementedError(f"Implement `get_initial` on {self.__class__.__name__}")

    def get_form_kwargs(self, view):
        return {}

    def get_step_data(self, form):
        return form.cleaned_data
