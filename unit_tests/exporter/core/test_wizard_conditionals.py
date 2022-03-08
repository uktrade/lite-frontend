import pytest

from exporter.core.wizard.conditionals import C


class FakeWizard:
    TRUE = True
    FALSE = False


@pytest.fixture
def wizard():
    return FakeWizard()


def is_true(wizard):
    return wizard.TRUE


def is_false(wizard):
    return wizard.FALSE


def test_unary_conditional(wizard):
    assert C(is_true)(wizard)
    assert not C(is_false)(wizard)


def test_not_conditional(wizard):
    assert not (~C(is_true))(wizard)
    assert (~C(is_false))(wizard)


def test_and_conditionals(wizard):
    assert (C(is_true) & C(is_true))(wizard)
    assert not (C(is_true) & C(is_false))(wizard)
    assert not (C(is_false) & C(is_true))(wizard)
    assert not (C(is_false) & C(is_false))(wizard)


def test_or_conditionals(wizard):
    assert (C(is_true) | C(is_true))(wizard)
    assert (C(is_true) | C(is_false))(wizard)
    assert (C(is_false) | C(is_true))(wizard)
    assert not (C(is_false) | C(is_false))(wizard)


def test_complex_conditionals(wizard):
    assert (C(is_true) & C(is_false) | C(is_true))(wizard)
    assert not ((~C(is_true)) & (C(is_false) | C(is_true)))(wizard)
