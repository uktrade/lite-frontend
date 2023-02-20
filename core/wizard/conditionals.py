class BaseConditional:
    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        if not isinstance(other, BaseConditional):
            raise TypeError(f"{type(other)} is not a Conditional")
        return And(self, other)

    def __or__(self, other):
        if not isinstance(other, BaseConditional):
            raise TypeError(f"{type(other)} is not a Conditional")
        return Or(self, other)


class Not(BaseConditional):
    def __init__(self, conditional):
        self.conditional = conditional

    def __call__(self, wizard):
        return not self.conditional(wizard)

    def __repr__(self):
        return f"<Not: {self.conditional}>"


class And(BaseConditional):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, wizard):
        return self.left(wizard) and self.right(wizard)

    def __repr__(self):
        return f"<And: {self.left} & {self.right}>"


class Or(BaseConditional):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, wizard):
        return self.left(wizard) or self.right(wizard)

    def __repr__(self):
        return f"<Or: {self.left} | {self.right}>"


class C(BaseConditional):
    def __init__(self, conditional_func):
        self.conditional_func = conditional_func

    def __call__(self, wizard):
        return self.conditional_func(wizard)

    def __repr__(self):
        return f"<C: {self.conditional_func.__name__}>"


class Flag(BaseConditional):
    def __init__(self, flag, key=None):
        self.flag = flag
        self.key = key

    def __call__(self, wizard):
        if self.key:
            return getattr(self.flag, self.key)
        return self.flag

    def __repr__(self):
        return f"<Flag: {self.flag} {self.key}>"
