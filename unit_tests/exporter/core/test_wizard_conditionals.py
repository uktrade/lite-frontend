import pytest

from exporter.core.wizard.conditionals import C, Flag


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


def test_only_compose_with_composables():
    with pytest.raises(TypeError):
        C(is_true) & is_true

    with pytest.raises(TypeError):
        C(is_true) | is_false


def test_flag(wizard):
    assert Flag(True)(wizard)
    assert not (~Flag(True))(wizard)
    assert (Flag(True) & Flag(True))(wizard)
    assert (Flag(True) | Flag(True))(wizard)


def test_flag_with_key(wizard):
    class Holder:
        true = True

    assert Flag(Holder, "true")(wizard)
    assert not (~Flag(Holder, "true"))(wizard)
    assert (Flag(Holder, "true") & Flag(Holder, "true"))(wizard)
    assert (Flag(Holder, "true") | Flag(Holder, "true"))(wizard)
