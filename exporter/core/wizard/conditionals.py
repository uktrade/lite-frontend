class BaseConditional:
    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)


class Not(BaseConditional):
    def __init__(self, conditional):
        self.conditional = conditional

    def __call__(self, wizard):
        return not self.conditional(wizard)


class And(BaseConditional):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, wizard):
        return self.left(wizard) and self.right(wizard)


class Or(BaseConditional):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, wizard):
        return self.left(wizard) or self.right(wizard)


class C(BaseConditional):
    def __init__(self, conditional_func):
        self.conditional_func = conditional_func

    def __call__(self, wizard):
        return self.conditional_func(wizard)
